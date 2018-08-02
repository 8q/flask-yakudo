$('#file-input-btn').click(() => {
    $('#file-input').click();
});

$('#file-input').change(event => {
    const $input = $(event.target);
    const file = $input.prop('files')[0];
    $('#cover').val(file.name);

    Promise.resolve(file)
        .then(file => {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = event => {
                    resolve(event.target.result);
                }
                reader.readAsDataURL(file);
            })
        })
        .then(imgSrc => {
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.onload = event => {
                    resolve(event.target);
                }
                img.src = imgSrc;
            })
        })
        .then(img => {
            const $canvas = $('#dummy');
            const ctx = $canvas[0].getContext('2d');
            let [w, h] = [img.width, img.height];
            if (w > 1000 || h > 1000) {
                [w, h] = w > h ? [1000, (1000 * h / w)] : [(1000 * w / h), 1000];
            }
            $canvas.attr('width', w);
            $canvas.attr('height', h);
            ctx.drawImage(img, 0, 0, w, h);
        });
});

function canvas2blob(canvas) {
    var type = 'image/jpeg';
    var bin = window.atob(canvas.toDataURL(type).split(',')[1]);
    var buffer = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) {
        buffer[i] = bin.charCodeAt(i);
    }
    var blob = new Blob([buffer.buffer], { type: type });
    return blob
}

$('#submit-btn').click(() => {
    const $canvas = $('#dummy');
    const blob = canvas2blob($canvas[0]);
    const formData = new FormData();
    formData.append('file', blob, 'upload.jpg');
    const win = window.open("");
    win.document.body.innerHTML = "loading...";

    $.ajax({
        async: false,
        type: 'POST',
        url: '/upload',
        data: formData,
        dataType: 'binary',
        responseType: 'blob',
        processData: false,
        contentType: false,
    })
    .done(data => {
        const blob = new Blob([data], { type: 'image/jpeg' });
        Promise.resolve(blob)
            .then(blob => {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = event => {
                        resolve(event.target.result);
                    }
                    reader.readAsDataURL(blob);
                });
            })
            .then(uri => {
                const image = new Image();
                image.src = uri;
                win.document.write(image.outerHTML);
            });
    });

    return false;
});
