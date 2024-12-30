const HOST = window.location.host;
const FULL_HOST = `${window.location.protocol}//${HOST}`;
const SESSION = Cookies.get('session');

function send_message(websocket) {
    const form = $('.form');
    const button = form.find('.submit');

    button.off('click').on('click', (e) => {
        e.preventDefault();

        const message = form.find('textarea').val();
        if (!message) return;

        if (websocket.readyState === WebSocket.OPEN) {
            websocket.send(JSON.stringify({ message }));
        } else {
            console.error('WS connection is closed');
        }
    });
}

function generate_current_time() {
    const date = new Date();
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const hours = date.getHours();
    const minutes = date.getMinutes();

    return `${hours}:${minutes}, ${day}.${month}.${year}`;
}

async function insert_block_to_history(childrens) {
    const current_time = generate_current_time();
    const data = {
        dialog: {
            created_at: current_time,
            replicas: []
        }
    }

    childrens.each((_, child) => {
        let text, source;
        const $child = $(child);
        
        const text_block = $child.find('.text');
        text = text_block !== null ? text_block.text() : '';    
        source = $child.hasClass('user') ? 'user' : 'ai';
        
        data.dialog.replicas.push(
            {
                source: source,
                text: text,
            }
        )
    })

    try {
        const request = await axios.post(
            `${FULL_HOST}/chat/api/dialog`,
            data, 
            { session: SESSION }
        )
        const { status, errors } = request.data;
        if (status === 'error') {
            errors.forEach(err => console.error(err))
        }
    } catch (error) {
        console.error(error.message)
    }

    // const chat_history_block = $('.chat-history');
    // chat_history_block.prepend(`
    //     <div class="history-point border border-1 border-light rounded-3 shadow w-100 p-3 text-center mb-4">
    //         Dialog from ${current_time}
    //     </div>
    // `);

    // return chat_history_block.scrollTop(0);

    window.location.reload();
}

function insert_block_to_dialog(message, whose = 'user') {
    const dialog = $('.dialog');
    let block;

    if (whose === 'user') {
        block = `
            <div class="user row row-lg-2 row-md-1 row-sm-1 mx-2 mb-4">
                <div class="col-6"></div>
                <div class="col-6 border border-1 border-light rounded-3 shadow p-4">
                    <span class="fw-bold text">${message}</span>
                </div>
            </div>

            <div class="ai row row-lg-2 row-md-1 row-sm-1 mx-2 mb-4">
                <div class="col-6 border border-1 border-light rounded-3 shadow p-4">
                    <span class="fw-bold text">...</span>
                </div>
                <div class="col-6"></div>
            </div>
        `;
    } else {
        dialog.children().last().remove();
        block = `
            <div class="ai row row-lg-2 row-md-1 row-sm-1 mx-2 mb-4">
                <div class="col-6 border border-1 border-light rounded-3 shadow p-4">
                    <span class="fw-bold text">${message}</span>
                </div>
                <div class="col-6"></div>
            </div>
        `;
    }

    dialog.append(block);
    return scroll_to_down_dialog(dialog);
}

function load_chat() {
    const WS_HOST = `ws://${HOST}1/ws/chat`;
    const websocket = new WebSocket(WS_HOST);

    websocket.onmessage = (e) => {
        const { message, from } = JSON.parse(e.data);
        insert_block_to_dialog(message, from);
    };

    send_message(websocket);
}

function scroll_to_down_dialog(dialog = null) {
    if (!dialog) dialog = $('.dialog');
    return dialog.scrollTop(dialog.prop('scrollHeight'));
}

function save_dialog() {
    const form = $('.form');
    const button = form.find('.save-dialog');

    button.off('click').on('click', async (e) => {
        e.preventDefault();

        const dialog = $('.dialog');
        const childrens = dialog.children();
        if (childrens.length) {
            await insert_block_to_history(childrens);
            dialog.empty();
        }
    });
}

function delete_dialog() {
    const delete_dialog_button = $('.delete-dialog');
    delete_dialog_button.off('click').on('click', async (e) => {
        e.preventDefault();
        const dialog_index = $(e.currentTarget).attr('dialog_index');
        if (dialog_index === undefined) {
            return;
        }
        
        try {
            const request = await axios.delete(
                `${FULL_HOST}/chat/api/dialog?dialog_index=${dialog_index}`,
                { session: SESSION }
            );
            const { status, errors } = request.data;
            if (status === 'error') {
                errors.forEach(err => console.error(err))
            }
        } catch (error) {
            console.error(error.message);
        }

        window.location.reload();
    })
}

function load_dialog() {
    const load_dialog_button = $('.load-dialog');
    load_dialog_button.off('click').on('click', async (e) => {
        e.preventDefault();
        const dialog_index = $(e.currentTarget).attr('dialog_index');
        if (dialog_index === undefined) {
            return;
        }
        
        try {
            const request = await axios.get(
                `${FULL_HOST}/chat/api/dialog?dialog_index=${dialog_index}`,
                { session: SESSION }
            );
            const { status, errors, dialogs } = request.data;
            if (status === 'error') {
                errors.forEach(err => console.error(err))
            } else {
                const replicas = dialogs.dialogs[0].replicas;
                replicas.forEach(replica => insert_block_to_dialog(replica.text, replica.source))
            }
        } catch (error) {
            console.error(error.message);
        }

        // window.location.reload();
    })
}

$(document).ready(() => {
    load_chat();
    scroll_to_down_dialog();
    save_dialog();
    load_dialog();
    delete_dialog();
});
