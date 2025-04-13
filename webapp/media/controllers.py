import datetime
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort
from .models import db, Actor, Movie, Director

from .forms import CommentForm, MovieForm

media_blueprint = Blueprint(
    'media',
    __name__,
    template_folder='../templates/media',
    url_prefix="/media"
)


# def sidebar_data():
#     recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
#     top_tags = db.session.query(
#         Tag, func.count(tags.c.post_id).label('total')
#     ).join(tags).group_by(Tag).order_by(desc('total')).limit(5).all()

#     return recent, top_tags


@media_blueprint.route('/')
@media_blueprint.route('/<int:page>')
def home(page=1):
    movies = Movie.query.all() 

    return render_template(
        'home.html',
        movies=movies
    )


@media_blueprint.route('/create', methods=['GET', 'POST'])
def create_entry():
    form = MovieForm()
    if form.validate_on_submit():
        new_entry = Movie()
        new_entry.title = form.title.data
        new_entry.director = form.director.data
        new_entry.actors = package_cast(form.actors.data)
        new_entry.year = form.year
        db.session.add(new_entry)
        db.session.commit()
        flash('Entry added', 'info')
        return redirect(url_for('.read_entry', movie_id=new_entry.id))   # this may not exist yet
    return render_template('create.html', form=form)

def package_cast(data):
    raw_cast = data
    actor_list = raw_cast.split(",")
    actors = []
    for str_actor in actor_list:
        name = str_actor.split(' ')
        actor = Actor(first_name=name[0], last_name=name[1])
        actors.append(actor)
    return actors

@media_blueprint.route('/read/<int:movie_id>', methods=['GET', 'POST'])
def read_entry(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    form = MovieForm()
    form.title.data = movie.title
    form.director.data = movie.director
    form.actors.data = movie.actors_to_string()
    form.year.data = movie.year
    return render_template('read.html', form=form, movie=movie)

@media_blueprint.route('/update/<int:movie_id>', methods=['GET', 'POST'])
def update_entry(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    form = MovieForm()
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.actors = package_cast(form.actors.data)
        movie.year = form.year.data
        movie.DateViewed = datetime.datetime.now()
        db.session.merge(movie)
        db.session.commit()
        return redirect(url_for('.display', movie_id=movie.id))
    form.title.data = movie.title
    form.director.data = movie.director
    form.actors.data = movie.actors_to_string()
    form.year.data = movie.year
    return render_template('update.html', form=form, movie=movie)
    
@media_blueprint.route('/delete/<int:movie_id>', methods=['GET', 'POST'])
def delete_entry(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    form = MovieForm()
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.actors = package_cast(form.actors.data)
        movie.year = form.year.data
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('.home', movie_id=movie.id))
    form.title.data = movie.title
    form.director.data = movie.director
    form.actors.data = movie.actors_to_string()
    form.year.data = movie.year
    return render_template('delete.html', form=form, movie=movie)

# @media_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
# def post(post_id):
#     form = CommentForm()

#     if form.validate_on_submit():
#         new_comment = Comment()
#         new_comment.name = form.name.data
#         new_comment.text = form.text.data
#         new_comment.post_id = post_id
#         try:
#             db.session.add(new_comment)
#             db.session.commit()
#         except Exception as e:
#             flash('Error adding your comment: %s' % str(e), 'error')
#             db.session.rollback()
#         else:
#             flash('Comment added', 'info')
#         return redirect(url_for('blog.post', post_id=post_id))

    # post = Post.query.get_or_404(post_id)
    # tags = post.tags
    # comments = post.comments.order_by(Comment.date.desc()).all()
    # recent, top_tags = sidebar_data()

    # return render_template(
    #     'post.html',
    #     post=post,
    #     tags=tags,
    #     comments=comments,
    #     recent=recent,
    #     top_tags=top_tags,
    #     form=form
    # )


# @media_blueprint.route('/tag/<string:tag_name>')
# def posts_by_tag(tag_name):
#     tag = Tag.query.filter_by(title=tag_name).first_or_404()
#     posts = tag.posts.order_by(Post.publish_date.desc()).all()
#     recent, top_tags = sidebar_data()

#     return render_template(
#         'tag.html',
#         tag=tag,
#         posts=posts,
#         recent=recent,
#         top_tags=top_tags
#     )


# @media_blueprint.route('/user/<string:username>')
# def posts_by_user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = user.posts.order_by(Post.publish_date.desc()).all()
#     recent, top_tags = sidebar_data()

#     return render_template(
#         'user.html',
#         user=user,
#         posts=posts,
#         recent=recent,
#         top_tags=top_tags
#     )
