var CommentComponent = React.createClass({
	getInitialState: function() {
		return ({
			page: this.props.comments.page,
			entity: this.props.comments.entity,
			comments: [],
			currentUser : []
		});
	},
	componentWillMount: function() {
		this.handleBlockUI();
	},
	componentDidUpdate: function() {
		this.handleBlockUI();
	},
	componentDidMount: function() {
		this.handleLoadData();
	},
	handleBlockUI: function() {
		var root = this;
		jQuery("#commentReact").block({
            message: "<img src="+this.props.loadingSrc+" />",
            css: {
                border: 'none',
                backgroundColor: 'argb(255,255,255,255)',
                marginTop: '50px'
            },
            fadeIn: 0,
            fadeOut: 0,
            overlayCSS:  {
                backgroundColor: '#FFF',
                opacity:         1,
                cursor:          'wait'
            },
        });
	},
	handleLoadData: function() {
		var record = {
			idPage: this.state.page,
			entity: this.state.entity
		};
		this.serverRequest = jQuery.post('/comment/load_comment', record ,function (result) {
		  var comments = result.data.record
	      this.setState({
					comments: comments.comments,
					currentUser: comments.currentUser
				});

	      jQuery("#commentReact").unblock();
	    }.bind(this));
	},
	handleSubmitComment: function(commentText) {
		var root = this;
		record = {
			content: commentText,
			idPage: this.state.page,
			entity: this.state.entity,
		}
		jQuery.ajax({
			url: '/comment/submit_comment',
			data: record,
			dataType: 'json',
			type: "post",
			success: function(data) {
				root.handleLoadData();
			},
			error: function(error) {}
		});
		// Clean
	},
	handleSubmitReply: function(idComment, commentText) {

		var root = this;
		var record = {
			content: commentText,
			idPage: this.state.page,
			entity: this.state.entity,
			idUser: 1,
			root: idComment
		}
		jQuery.ajax({
			url: '/comment/reply_comment',
			data: record,
			dataType: 'JSON',
			type: "POST",
			success: function(data) {
				root.handleLoadData();
			},
			error: function() {}
		});
		// Clean
	},
	handleLikeComment: function(idComment) {
		var root = this;
		jQuery.ajax({
			url: '/comment/like_comment',
			data: {idComment: idComment, idUser: 1 },
			dataType: "JSON",
			type: "POST",
			success: function(data) {
				root.handleLoadData();
			},
			error: function() {}
		});
	},
	handleDislikeComment: function(idComment) {
		var root = this;
		jQuery.ajax({
			url: '/comment/dislike_comment',
			data: {idComment: idComment, idUser: 1 },
			dataType: "JSON",
			type: "POST",
			success: function(data) {
				root.handleLoadData();
			},
			error: function() {}
		});
	},
	render: function() {
		return (
			React.createElement('div', {className: 'commnt_secs'},
				React.createElement('h1', {className: 'green_border_txt'}, "Comment & Discuss"),
				React.createElement('div', {className: 'commnt_box'},
					React.createElement('h2', {}, "All comments ("+this.state.comments.length+")"),
					React.createElement(CommentForm, {
						handleSubmitComment: this.handleSubmitComment,
						currentUser: this.state.currentUser
					}),
					React.createElement(Comments, {
						comments: this.state.comments,
						handleLikeComment: this.handleLikeComment,
						handleDislikeComment: this.handleDislikeComment,
						handleSubmitReply: this.handleSubmitReply
					})
				),
				React.createElement('div', {className: 'clearfix'})
			)
		);
	}
});

var CommentForm = React.createClass({
	propTypes: {
		handleSubmitComment: React.PropTypes.func
	},
	handleSubmitComment: function() {
		var commentText = this.refs.commentText.value;
		if ((commentText).trim().length > 0) {
			this.props.handleSubmitComment(commentText);
	    // Clean
	    this.handleHideForm();
		}
	},
	handleShowForm: function() {
		// Close all opening other
		jQuery(".reply-form").each(function(i, element){
			jQuery(this).css('display', 'none');
		});
		var element = document.getElementById("comment-form-btns");
		element.style.display = 'inline';
	},
	handleHideForm: function() {
		this.refs.commentText.value = '';
		var element = document.getElementById("comment-form-btns");
		jQuery('.form-control').blur();
		element.style.display = 'none';
	},
	handleFormValidation: function() {
		var len = (this.refs.commentText.value).trim().length;
		document.getElementById('post_btn-comment').className = ((len>0) ? "btn-s-green clickable" : "btn-s-green disabled-btn clickable");
	},
	render: function() {
		var root = this;
		var attr = {};
		attr.id = 'comment-form-btns';
		attr.className = 'smll_pag_ul comment_form';

    var attrCancel = {};
  	attrCancel.id = 'cancel_btn-comment';
  	attrCancel.className = 'btn-s-blue clickable';
		attrCancel.onClick = this.handleHideForm;

		var attrPost = {};
		attrPost.id = 'post_btn-comment';
  	attrPost.className = 'disabled-btn btn-s-green clickable';
		attrPost.onClick = this.handleSubmitComment;

  	var attrCommentText = {};
    attrCommentText.className = 'form-control';
		attrCommentText.onClick = this.handleShowForm;
		attrCommentText.onChange = this.handleFormValidation;
		attrCommentText.ref = 'commentText';
		attrCommentText.placeholder = 'Add a public comment...';
		// attrCommentText.onBlur = this.handleHideForm;
		attrCommentText.onKeyPress = function(event) {
			if (event.key == 'Enter') {
				root.handleSubmitComment();
			}
		};
		var attrImage = {
				// src: this.props.currentUser.image,
				src: '/static/genopedia/images/demo_user1.jpg',
				className: 'img-responsive'
			};
		return (
			React.createElement('div', {},
				React.createElement('ul',  {className: 'commnt_box_ul'},
					React.createElement('li', {},
						React.createElement('a', {},
							React.createElement('img',attrImage)
						)
					),
					React.createElement('li', {},
						React.createElement('img',{className: 'pos_img'}),
						React.createElement('textarea', attrCommentText),
						React.createElement('ul', attr,
							React.createElement('li', {style: {'paddingRight': 0}},
								React.createElement('div', attrCancel, 'Cancel')
							),
							React.createElement('li', {style: {'paddingRight': 0}},
								React.createElement('div', attrPost, 'Post')
							)
						)
					)
				)
			)
		);
	}
});

var Comments = React.createClass({
	propTypes: {
		comments: React.PropTypes.array,
		handleSubmitReply: React.PropTypes.func,
		handleLikeComment: React.PropTypes.func,
		handleDislikeComment: React.PropTypes.func,
		handleOnchangeReply: React.PropTypes.func
	},
	renderReplies: function(data) {
		var elements = [];
		var root = this;
		data.map(function(rpl, k) {
			var element =
				React.createElement(Comment, {key: k, comment: rpl,
					handleSubmitReply: root.props.handleSubmitReply,
					handleLikeComment: root.props.handleLikeComment,
					handleDislikeComment: root.props.handleDislikeComment}
				);
			elements.push(element);
		});
		return elements;
	},
	renderComments: function() {
		var elements = [];
		var root = this;
		this.props.comments.map(function(cmt, k) {
			var element =
				React.createElement(Comment, {key: k, comment: cmt,
					handleSubmitReply: root.props.handleSubmitReply,
					handleLikeComment: root.props.handleLikeComment,
					handleDislikeComment: root.props.handleDislikeComment,
					replies: root.renderReplies(cmt.replies)}
				);
			elements.push(element);
		});
		return elements;
	},
	render: function() {
		return (
			React.createElement('div', {},
				this.renderComments()
			)
		);
	}
});

var Comment = React.createClass({
	propTypes: {
		comment: React.PropTypes.object,
		handleSubmitReply: React.PropTypes.func,
		handleLikeComment: React.PropTypes.func,
		handleDislikeComment: React.PropTypes.func,
	},
	handleSubmitReply: function(comment) {
		var commentText = (this.refs.commentText.value).trim();
		if (commentText.length > 0) {
			this.props.handleSubmitReply(comment.root, commentText);
			this.handleHideForm('reply-form-'+comment.id);
		}
	},
	handleLikeComment: function(idComment) {
		this.props.handleLikeComment(idComment);
	},
	handleDislikeComment: function(idComment) {
		this.props.handleDislikeComment(idComment);
	},
	handleShowForm: function(name) {
		// Close Main comment
		var element = document.getElementById("comment-form-btns");
		element.style.display = 'none';
		// Close all opening other
		jQuery(".reply-form").each(function(i, element){
			jQuery(this).css('display', 'none');
		});
		var element = document.getElementById(name);
		element.style.display = 'inline';
		this.refs.commentText.focus();
	},
	handleHideForm: function(name) {
		this.refs.commentText.value = '';
		var element = document.getElementById(name);
		element.style.display = 'none';
		jQuery('.form-control').blur();
	},
	handToggleReplies: function(form, viewReplies, numReplies) {
		var elementForm = document.getElementById(form);
		var elementViewReplies = document.getElementById(viewReplies);
		if (elementForm.style.display == 'none') {
			elementForm.style.display = 'inline';
			elementViewReplies.textContent = ("Hide " + numReplies + " " +((numReplies > 1) ? 'replies' : 'reply'));
		} else {
			elementForm.style.display = 'none';
			elementViewReplies.textContent = ("View " + numReplies + " " +((numReplies > 1) ? 'replies' : 'reply'));
		}
	},
	handleFormValidation: function(id) {
		var len = (this.refs.commentText.value).trim().length;
		var className = 'post_btn-'+id.toString();
		document.getElementById(className).className = ((len>0) ? "btn-s-green clickable" : "btn-s-green disabled-btn clickable");
	},
	handleLongComment: function(comment) {
		var len = comment.content.length;
		var id = 'comment-content-'+comment.id;
		var element;

		if (len > 150) {
			var headContent = comment.content.substring(0, 150);
			var tailContent = comment.content.substring(150, len);
			element =
				React.createElement('div', {},
					React.createElement('input', {id: id, type: 'checkbox', className: 'read-more-state'}),
					React.createElement('p', {className: 'read-more-wrap content-limit'},
						React.createElement('text', {className: 'semibold_txt'}, headContent),
						React.createElement('span', {className: 'read-more-target'}, tailContent)
					),
					React.createElement('label', {htmlFor: id, className: 'read-more-trigger'})
				)
		} else {
			element = React.createElement('p', {className: 'semibold_txt'}, this.props.comment.content);
		}
		return element;
	},
	render: function() {
		var root = this;
		var attrReplies = {};
			attrReplies.style = {};
			attrReplies.style.display = "none";
			attrReplies.id = "replies-comment-"+this.props.comment.id;

			var attrViewRepl = {};
			attrViewRepl.className = 'blue semibold_txt';
			attrViewRepl.id = 'view-replies-text-'+this.props.comment.id;
			attrViewRepl.style = {};
			attrViewRepl.style.cursor = 'pointer';
      attrViewRepl.text = (this.props.comment.numReply > 0) ? "View " + this.props.comment.numReply + " " +((this.props.comment.numReply > 1) ? 'replies' : 'reply') : '';
			attrViewRepl.onClick = this.handToggleReplies.bind(null, "replies-comment-"+this.props.comment.id, 'view-replies-text-'+this.props.comment.id, this.props.comment.numReply);

			var attr = {};
			attr.style = {};
			attr.style.display = 'none';
			attr.className = 'reply-form';
			attr.id = 'reply-form-'+this.props.comment.id;

			var attrthumbsUp = {};
			attrthumbsUp.style = {};
			attrthumbsUp.style.cursor = 'pointer';
			attrthumbsUp.className = 'fa fa-thumbs-up';
			attrthumbsUp.onClick = this.props.handleLikeComment.bind(null, this.props.comment.id);

			var attrthumbsDown = {};
			attrthumbsDown.style = {};
			attrthumbsDown.style.cursor = 'pointer';
			attrthumbsDown.className = 'fa fa-thumbs-down';
			attrthumbsDown.onClick = this.props.handleDislikeComment.bind(null, this.props.comment.id);

      var replyBtn = {};
			replyBtn.className = 'reply-comment-btn'
    	replyBtn.onClick = this.handleShowForm.bind(null, 'reply-form-'+this.props.comment.id);

      var attrFormBtn = {};
			attrFormBtn.id = 'comment-form-btns';
			attrFormBtn.className = 'smll_pag_ul reply_form';

      var attrCancel = {};
    	attrCancel.className = 'btn-s-blue clickable';
    	attrCancel.id = 'cancel_btn-'+this.props.comment.id;
  		attrCancel.onClick = this.handleHideForm.bind(null, 'reply-form-'+this.props.comment.id);

			var attrPost = {};
    	attrPost.className = 'disabled-btn btn-s-green clickable';
    	attrPost.id = 'post_btn-'+this.props.comment.id;
  		attrPost.onClick = this.handleSubmitReply.bind(null, this.props.comment);

			var attrCommentText = {};
	    attrCommentText.className = 'form-control';
			attrCommentText.onChange = this.handleFormValidation.bind(null, this.props.comment.id);
			attrCommentText.ref = 'commentText';
			// attrCommentText.onBlur = this.handleHideForm.bind(null, 'reply-form-'+this.props.comment.id);
			attrCommentText.placeholder = 'Add a public comment...';
			attrCommentText.onKeyPress = function(event) {
				if (event.key == 'Enter') {
					root.handleSubmitReply(root.props.comment);
				}
			}
			var attrImage = {
					// src: this.props.comment.image,
					src: '/static/genopedia/images/demo_user1.jpg',
					className: 'img-responsive'
			};
		return (
			React.createElement('ul', {className: 'commnt_box_ul responsive_s'},
				React.createElement('li', {},
					React.createElement('a', {},
						React.createElement('img', attrImage)
					)
				),
				React.createElement('li', {},
					React.createElement('p', {className: 'bold_txt'},
						React.createElement('a', {className: 'blue'}, this.props.comment.userName),
						React.createElement('span', {}, this.props.comment.createdAt)
					),
					this.handleLongComment(this.props.comment),
					React.createElement('ul', {className: 'smll_pag_ul'},
						React.createElement('li', replyBtn, 'Reply'),
						React.createElement('li', {}, '-'),
						React.createElement('li', {className: 'blue semibold_txt'}, this.props.comment.numLike),
						React.createElement('li', {},
							React.createElement('span', {}),
							React.createElement('i', attrthumbsUp)
						),
						React.createElement('li', {},
							React.createElement('span', {}, this.props.comment.numDislike),
							React.createElement('i', attrthumbsDown)
						),
						React.createElement('li', {},
							React.createElement('a', attrViewRepl, attrViewRepl.text)
						)
					),
					React.createElement('div', attrReplies,
						this.props.replies
					),
					// Reply Form
					React.createElement('div', attr,
						React.createElement('ul',  {className: 'commnt_box_ul'},
							React.createElement('li', {},
								React.createElement('a', {},
									React.createElement('img',attrImage)
								)
							),
							React.createElement('li', {},
								React.createElement('img',{className: 'pos_img'}),
								React.createElement('textarea', attrCommentText),
								React.createElement('ul', attrFormBtn,
									React.createElement('li', {style: {'paddingRight': 0}},
										React.createElement('div', attrCancel, 'Cancel')
									),
									React.createElement('li', {style: {'paddingRight': 0}},
										React.createElement('div', attrPost, 'Reply')
									)
								)
							)
						)
					)
				)
			)
		);
	}
});
