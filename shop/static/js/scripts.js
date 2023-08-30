function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}

const forms = document.querySelector('form[name=js-filter]');

forms.addEventListener('submit', function (e) {
    // Получаем данные из формы
    e.preventDefault();
    let url = this.action;
    let params = new URLSearchParams(new FormData(this)).toString();
    ajaxSend(url, params);
});

function render(data) {
    // Рендер шаблона
    let template = Hogan.compile(html);
    let output = template.render(data);

    const div = document.querySelector('.left-ads-display>.row');
    div.innerHTML = output;
}

let html = '\
{{#movies}}\
    <div class="col-lg-3">\
        <div class="box-element product">\
            <div class="card mb-4 rounded-2 shadow-sm">\
                <div class="card-header py-3">\
                    <h2>{{ book.name }} </h2>\
                </div>\
                \
                <div class="card-body">\
                    <h1 class="card-title pricing-card-title">${{ book.price }}<small class="text-body-secondary fw-light"></small></h1>\
                    <ul class="list-unstyled mt-3 mb-4">\
                        <p><img width="70%" src="media/{{ book.image.url }}" alt=""></p>\
                    </ul>\
<input type="button" class="w-100 btn btn-lg btn-outline-primary" value="Add to Cart" />\
<div class="modal fade" id="modal-contact-us" tabindex="-1" aria-labelledby="contact_us" aria-hidden="true">\
                                        <div class="modal-dialog">\
                                            <div class="modal-content">\
\
                                            </div>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                            <hr>\
               <a class="w-100 btn btn-lg btn-success" href="{% url "shop:book-detail" book.pk book.slug %}">View</a>\
                        </div>\
                    </div>\
{{/movies}}'