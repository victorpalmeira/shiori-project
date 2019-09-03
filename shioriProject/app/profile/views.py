# app/profile/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import profile
from forms import BookmarkForm
from .. import db
from ..models import Bookmark


# Bookmark Views


@profile.route('/bookmarks', methods=['GET', 'POST'])
@login_required
def list_bookmarks():
    """
    List all bookmarks
    """
    
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()

    return render_template('profile/bookmarks/bookmarks.html', bookmarks=bookmarks, title="Bookmarks")


@profile.route('/bookmarks/add', methods=['GET', 'POST'])
@login_required
def add_bookmark():
    """
    Add a bookmark to the database
    """

    add_bookmark = True

    form = BookmarkForm()
    if form.validate_on_submit():
        bookmark = Bookmark(name=form.name.data, url=form.url.data, description=form.description.data, user_id=current_user.id)
        try:
            # add bookmark to the database
            db.session.add(bookmark)
            db.session.commit()
            flash('You have successfully added a new bookmark.')
        except:
            # in case bookmark name already exists
            flash('Error: bookmark name already exists.')

        # redirect to bookmarks page
        return redirect(url_for('profile.list_bookmarks'))

    # load bookmark template
    return render_template('profile/bookmarks/bookmark.html', action="Add", add_bookmark=add_bookmark, form=form, title="Add Bookmark")


@profile.route('/bookmarks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(id):
    """
    Edit a bookmark
    """

    add_bookmark = False

    bookmark = Bookmark.query.get_or_404(id)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        bookmark.name = form.name.data
        bookmark.url = form.url.data
        bookmark.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the bookmark.')

        # redirect to the bookmarks page
        return redirect(url_for('profile.list_bookmarks'))

    form.description.data = bookmark.description
    form.url.data = bookmark.url
    form.name.data = bookmark.name
    return render_template('profile/bookmarks/bookmark.html', action="Edit", add_bookmark=add_bookmark, form=form, bookmark=bookmark, title="Edit Bookmark")


@profile.route('/bookmarks/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_bookmark(id):
    """
    Delete a bookmark from the database
    """

    bookmark = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark)
    db.session.commit()
    flash('You have successfully deleted the bookmark.')

    # redirect to the bookmarks page
    return redirect(url_for('profile.list_bookmarks'))

    return render_template(title="Delete Bookmark")
