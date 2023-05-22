"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import time

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A

from py4web.utils.form import Form, FormStyleBulma
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html',db, auth, url_signer)
def index():
    post = db(db.post.user_email == get_user_email()).select()
    return dict(
        # This is the signed URL for the callback.
        load_contacts_url = URL('load_contacts', signer=url_signer),
        add_contact_url = URL('add_contact', signer=url_signer),
        delete_contact_url = URL('delete_contact', signer=url_signer),
        edit_contact_url = URL('edit_contact', signer=url_signer),
        upload_thumbnail_url = URL('upload_thumbnail', signer=url_signer),
        post=post,
        my_callback_url=URL('my_callback', signer=url_signer),
    )
@action('my_callback')
@action.uses(url_signer.verify())
def my_callback():
    post = db(db.post).select(
        orderby=~db.post.id
    )
    return dict(post=post)
@action('add', method=['GET', 'POST'])
@action.uses(db, session, auth.user, 'add.html')
def addpost():
    form = Form(db.post, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('inc/<post_id:int>')
@action.uses(db, session, auth.user,'inc.html')
def likecount(post_id=None):
    post = db.post[post_id]
    if post is None:
        redirect(URL('index'))
    if post.user_email != get_user_email():
        redirect(URL('index'))
    post.like += 1
    post.update_record()
    redirect(URL('index'))

@action('edit/<post_id:int>', method=['GET', 'POST'])
@action.uses(db, session, auth.user, 'edit.html')
def editpost(post_id=None):
    assert post_id is not None
    p = db.post[post_id]
    if p is None:
        redirect(URL('index'))
    form = Form(db.post, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('delete/<post_id:int>')
@action.uses(db, session, auth.user, 'delete.htmls')
def deletepost(post_id=None):
    assert post_id is not None
    db(db.post.id == post_id).delete()
    redirect(URL('index'))

# This is our very first API function.
@action('load_contacts')
@action.uses(url_signer.verify(), db)
def load_contacts():
    rows = db(db.contact).select().as_list()
    return dict(rows=rows)

@action('add_contact', method="POST")
@action.uses(url_signer.verify(), db)
def add_contact():
    id = db.contact.insert(
        first_name=request.json.get('first_name'),
        last_name=request.json.get('last_name'),
    )
    return dict(id=id)

@action('delete_contact')
@action.uses(url_signer.verify(), db)
def delete_contact():
    id = request.params.get('id')
    assert id is not None
    db(db.contact.id == id).delete()
    return "ok"

@action('edit_contact', method="POST")
@action.uses(url_signer.verify(), db)
def edit_contact():
    # Updates the db record.
    id = request.json.get("id")
    field = request.json.get("field")
    value = request.json.get("value")
    print(id, field, value)
    db(db.contact.id == id).update(**{field: value})
    time.sleep(1) # debugging
    return "ok"

@action('upload_thumbnail', method="POST")
@action.uses(url_signer.verify(), db)
def upload_thumbnail():
    contact_id = request.json.get("contact_id")
    thumbnail = request.json.get("thumbnail")
    db(db.contact.id == contact_id).update(thumbnail=thumbnail)
    return "ok"
