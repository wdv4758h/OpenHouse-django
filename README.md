# Apache

pacman -S mod_wsgi2

/etc/httpd/conf/httpd.conf

    LoadModule wsgi_module modules/mod_wsgi.so

    # Django Settings

# Wsgi

- PYTHON_EGG_CACHE

os.environ['PYTHON_EGG_CACHE'] = os.path.dirname(os.path.dirname(__file__)) + '/.python-eggs'

# Salary

審核的部份用了 jQuery 做 Ajax Post
template list.html 裡有 class "pass/deny" 的 link
還有 class="status"
是作為抓判斷、審核用的

# Wagtail

## Child Box

在一些頁面會需要點擊後出現一個框框在最前面給使用者輸入一些東西，
wagtail 有做相關的東西叫作 Modal Work Flow，
先在 view 裡面

```python
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
```

接著撰寫需要的 template，並在 views.py 裡面使用

```python
return render_modal_workflow(request, 'salary/deny.html', 'salary/deny.js', {'id': salary_id})
```

template:

```html
{% include "wagtailadmin/shared/header.html" with title="退回" %}
<div class="nice-padding">
    <form action="{% url 'blablabla' %}" method="POST">
        {% csrf_token %}
        <div class="field char_field">
            <label for="id_bla">Bla:</label>
            <div class="field-content">
                <input id="id_bla" name="reason" type="text" required>
            </div>
        </div>
        <input type="submit" value="送出" />
    </form>
</div>
```

```javascript
// index.html
$(document).on('click', 'a.deny', function () {
    a = this;
    ModalWorkflow({
        'url': a.href,
        'responses': {
            'update': function (data) {
                $(a).parent().siblings('.status').replaceWith(data);
                return false;
            }
        }
    });
    return false;   // avoid direct to the link
});
```

```javascript
// deny.js
function(modal) {
    $('form', modal.body).submit(function() {
        $.ajax({
            type: 'POST',
            url: this.action,
            data: $(this).serialize(),
            success: function (data) { modal.respond('update', data); }
        });
        modal.close();
        return false;
    });
}
```
