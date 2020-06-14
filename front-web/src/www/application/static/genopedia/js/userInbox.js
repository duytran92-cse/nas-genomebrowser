var InboxMessage = React.createClass({
    getInitialState: function() {
        var data = this.props.data;
        return ({
            data: data,
            sender: data.sender,
            messShow: [],
            newMess: false,
            listUser: data.listUser,
            keyMessShow: '',
        });
    },
    onChangeState: function(item) {
        var temp = this.props.data;
        this.props.data.sender.map(function(val, key) {
            if (val.idSender === item.idSender) {
                temp.sender[key] = item;
            }
        });
        this.setState({
            data: temp,
            messShow: item,
            newMess: false,
            keyMessShow: item.idSender
        });
        jQuery('#uploadImageMess').modal('hide');
        jQuery('#sendVideo').modal('hide');
    },
    onNewMess: function(value) {
        this.setState({
            newMess: value
        })
    },
    onChangeDataSender: function(value) {
        this.setState({
            sender: value,
            newMess: false
        });
    },
    render: function() {
        return (
            React.createElement('div', {
                    className: 'main_cont'
                },
                React.createElement('div', {
                        className: 'container'
                    },
                    React.createElement('div', {
                            className: 'row'
                        },
                        React.createElement('div', {
                                className: 'bg_colr'
                            },
                            React.createElement('div', {
                                className: 'seperate_line_inbox'
                            }),
                            React.createElement('div', {
                                    className: 'col-md-3 col-sm-3 profile_right'
                                },
                                React.createElement(LeftInbox, {
                                    data: this.state.data,
                                    messShow: this.state.messShow,
                                    onChange: this.onChangeState,
                                    onChangeSender: this.onChangeDataSender,
                                    onNewMess: this.onNewMess,
                                    sender: this.state.sender,
                                    newMess: this.state.newMess,
                                    keyMessShow: this.state.keyMessShow
                                })
                            ),
                            React.createElement('div', {
                                    className: 'col-md-9 col-sm-9 inbox_right'
                                },
                                React.createElement(RightInbox, {
                                    messShow: this.state.messShow,
                                    data: this.state.data,
                                    onChange: this.onChangeState,
                                    newMess: this.state.newMess
                                })
                            ),
                            React.createElement('div', {
                                className: 'clearfix'
                            })
                        )
                    )
                )
            )
        );
    }
});

var RightInbox = React.createClass({
    componentDidMount: function() {
        jQuery('.selectpicker').selectpicker({
            style: 'form-control',
            size: 2
        });
    },
    renderFormReply:function () {
      var root = this;
        return (
          React.createElement('div', {
              className: 'clearfix'
          }),
          React.createElement('div', {
                  className: 'commnt_post_secs'
              },
              React.createElement('div', {
                      className: 'p_cmnt_s'
                  },
                  React.createElement('textarea', {
                      className: 'trans_textarea',
                      placeholder: 'Write a reply.....',
                      onKeyDown: function(e) {
                        if (e.keyCode == 13) {
                          var text = jQuery('#messReply-text').val();
                          if (text.trim() != '') {
                              this.replyMess(root, text);
                              var text = jQuery('#messReply-text').val('');
                          }
                        }
                      },
                      id: 'messReply-text'
                  }),
                  React.createElement('div', {
                          className: 'post_elemnt'
                      },
                      React.createElement('ul', {},
                          React.createElement('li', {},
                              React.createElement('a', {
                                      'data-toggle': 'modal',
                                      'data-target': '#uploadImageMess',
                                      href: '',
                                      'role': 'button',
                                  },
                                  React.createElement('i', {
                                      className: 'fa fa-camera'
                                  })
                              )
                          ),
                          React.createElement('li', {},
                              React.createElement('a', {
                                      'data-toggle': 'modal',
                                      'data-target': '#sendVideo',
                                      href: '',
                                      'role': 'button',
                                  },
                                  React.createElement('i', {
                                      className: 'fa fa-youtube-play'
                                  })
                              )
                          ),
                          React.createElement('li', {
                                  className: 'right',
                                  onClick: function() {
                                      var text = jQuery('#messReply-text').val();
                                      if (text.trim() != '') {
                                          this.replyMess(root, text);
                                          var text = jQuery('#messReply-text').val('');
                                      }
                                  }
                              },
                              React.createElement('a', {
                                  href: '#',
                                  className: 'reply_link'
                              }, 'Reply')
                          )
                      )
                  )
              )
          )
        )
    },
    renderMessBody: function() {
        var ele = [];
        var data = this.props.messShow;
        var styleTextTime = { fontStyle: 'italic'};
        this.props.messShow.message.map(function(item, key) {
            var attr = {
                className: (key == data.message.length - 1) ? 'inbox_secs' : 'inbox_secs border_bot'
            };
            var styleImg = {
                maxHeight: '200px'
            };
            var attrVi = {
                style: (item.messVid) ? {
                    height: '200px'
                } : {
                    width: '0px',
                    height: '0px'
                },
                className: (item.messVid) ? 'embed-responsive-item' : 'hidden',
                src: item.messVid
            }
            ele.push(
                React.createElement('div', attr,
                    React.createElement('div', {
                            className: 'col-md-1 com-sm-1'
                        },
                        React.createElement('a', {
                                href: '#'
                            },
                            React.createElement('img', {
                                src: item.imageSender,
                                className: 'round_img'
                            })
                        )
                    ),
                    React.createElement('div', {
                            className: 'col-md-11 com-sm-11'
                        },
                        React.createElement('p', {
                                className: 'bold_txt m_bot05'
                            },
                            React.createElement('a', {
                                href: '#'
                            }, item.nameSender),
                            React.createElement('span', {
                                    className: 'right tyml_txt'
                                },
                                React.createElement('i', {
                                    className: 'fa fa-clock-o'
                                },
                                    React.createElement('span', {style: styleTextTime},  " "+item.time)
                              )
                            )
                        ),
                        React.createElement('p', {
                            className: 'semibold_txt'
                        }, item.messText),
                        React.createElement('img', {
                            className: 'img-responsive',
                            style: styleImg,
                            src: item.messImage
                        }),
                        React.createElement('iframe', attrVi)
                    ),
                    React.createElement('div', {
                        className: 'clearfix m_bot10'
                    })
                )
            )
        });
        return ele;
    },
    renderSelectNewMess: function() {
      var styledivContent = {
          height: '500px'
      };
      var styleDivSelect = {
          display: 'inline-flex',
          width: '100%',
          padding: '10px 10px 0 10px'
      };
      var styleSelect = {
          marginLeft: '5px'
      };
      var ele = [];
      this.props.data.listUser.map(function(item, key){
          ele.push(
            React.createElement('option', {
              value: item.id,
              'data-content' : '<img src="'+item.img+'" style="height: 16px;width: 16px"/> <span style="display:inline-block; width:100px">'+item.name+'</span>'
            }
          )
        );
      });
      return (
        React.createElement('div', {
                id: 'div-new-mess',
                style: styleDivSelect,
                className: 'hidden'
            },
            React.createElement('span', {}, 'To: '),
            React.createElement('select', {
                    id: 'user-select',
                    'data-live-search': "true",
                    className: 'selectpicker'
                },
                ele
            )
        )
      );
    },
    render: function() {
        var root = this;
        var styleNote = {
            textAlign: 'center',
            paddingTop: '20px',
            paddingBottom: '50px'
        };
        var styleScroll = {
            maxHeight: '400px',
            minHeight: '100px',
            overflowY: 'auto',
            overflowX: 'hidden'
        };
        if (this.props.newMess) {
            jQuery('#div-new-mess').removeClass('hidden').attr('style', 'height:200px ;padding: 10px 10px 0 10px');
            jQuery('#div-content-mess').addClass('hidden');
            jQuery('#div-form-reply').removeClass('hidden');
        }
        else {
          jQuery('#div-new-mess').addClass('hidden');
          jQuery('#div-content-mess').removeClass('hidden');
        }
        jQuery('.selectpicker').selectpicker({
            style: 'form-control',
            size: 4
        });

        if (this.props.messShow.message) {
            return (
                React.createElement('div', {},
                    this.renderSelectNewMess(),
                    React.createElement('div', {id: 'div-content-mess'},
                        React.createElement('h1', {
                            className: 'inbox_border'
                        }, this.props.messShow.name),
                        React.createElement('div', {
                            className: 'clearfix m_bot20'
                        }),
                        React.createElement('div', {
                                style: styleScroll
                            },
                            this.renderMessBody()
                        )),
                        this.renderFormReply()
                )
            );
        } else {
            return (
                React.createElement('div', {},
                    this.renderSelectNewMess(),
                    React.createElement('h2', {
                        style: styleNote
                    }, 'No message preview'),
                    React.createElement('div', {id: 'div-form-reply', className:'hidden'}, this.renderFormReply())
                )
            );
        }
    }
});
var LeftInbox = React.createClass({
    renderSenderMessProfile: function() {
        var ele = [];
        var root = this;
        this.props.sender.map(function(item, key) {
          var classActive = (item.idSender == root.props.keyMessShow) ? 'messActive' : '';
            ele.push(
                React.createElement('li', {
                        onClick: function(e) {
                            item.unread = 0;
                            this.resetRead(root, item.idSender);
                            root.props.onChange(item);
                        },
                        className: classActive
                    },
                    React.createElement('div', {
                            className: 'user_s vert_mid'
                        },
                        React.createElement('img', {
                            src: item.image
                        }), (item.unread > 0) ?
                        React.createElement('span', {
                            className: 'vert_mid'
                        }, item.unread) : null
                    ),
                    React.createElement('div', {
                            className: 'user_name_r semibold_txt'
                        },
                        React.createElement('a', {}, item.name)
                    ),
                    React.createElement('div', {
                        className: 'clearfix'
                    })
                )
            );
        });
        return ele;
    },
    render: function() {
        var root = this;
        var styleScroll = {
            maxHeight: '400px',
            minHeight: '100px',
            overflowY: 'auto',
            overflowX: 'hidden'
        };
        return (
            React.createElement('div', {},
                React.createElement('h1', {}, 'Inbox'),
                React.createElement('div', {
                        className: 'search_input'
                    },
                    React.createElement('i', {
                        className: 'fa fa-search absolute_i'
                    }),
                    React.createElement('input', {
                        onChange: function(e) {
                            var keyword = jQuery(e.currentTarget).val();
                            var arraySender = [];
                            if (keyword.trim() != '') {
                                root.props.data.sender.map(function(item, val) {
                                    if (item.name.includes(keyword) || item.name == keyword) {
                                        arraySender.push(item);
                                    }
                                });
                                root.props.onChangeSender(arraySender);
                            } else {
                                root.props.onChangeSender(root.props.data.sender);
                            }
                        },
                        type: 'text',
                        className: 'form-control input_a',
                        placeholder: 'Search for name'
                    })
                ),
                React.createElement('div', {
                        className: 'right_p_bg'
                    },
                    React.createElement('ul', {},
                        React.createElement('li', {},
                            React.createElement('a', {
                                    href: '#',
                                    onClick: function() {
                                        root.props.onNewMess(true);
                                    },
                                    className: 'buttn2'
                                },
                                React.createElement('i', {
                                    className: 'fa fa-evenlope'
                                }),
                                'New Message'
                            )
                        ),
                        React.createElement('div', {
                                style: styleScroll
                            },
                            this.renderSenderMessProfile()
                        )
                    )
                ),
                React.createElement('div', {},
                    React.createElement(UploadImageInbox, {
                        messShow: root.props.messShow,
                        data: root.props.data,
                        onChange: root.props.onChange,
                        newMess: root.props.newMess
                    })
                ),
                React.createElement('div', {},
                    React.createElement(UploadLinkVideo, {
                        messShow: root.props.messShow,
                        data: root.props.data,
                        onChange: root.props.onChange,
                        newMess: root.props.newMess
                    })
                )
            )
        );
    }
});

function resetRead(root, idSender) {
    var formData = new FormData();
    formData.append('act', 'read');
    formData.append('id', JSON.stringify({
        idSender: root.props.data.profile.id,
        idReceiver: idSender
    }));
    var urlReplyMess = root.props.data.urlReplyMess;
    jQuery.ajax({
        type: "post",
        dataType: 'json',
        url: urlReplyMess,
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(result) {},
        error: function(result) {}
    });
}
function replyMess(root, text) {
  var formData = new FormData();
  formData.append('act', 'text');
  formData.append('data', text);
  if(root.props.newMess) {
    formData.append('id', JSON.stringify({
        idSender: root.props.data.profile.id,
        idReceiver: jQuery('#user-select').val()
    }));
  }
  else {
    formData.append('id', JSON.stringify({
        idSender: root.props.data.profile.id,
        idReceiver: root.props.messShow.idSender
    }));
  }
    var urlReplyMess = root.props.data.urlReplyMess;
    (function(root) {
        jQuery.ajax({
            type: "post",
            dataType: 'json',
            url: urlReplyMess,
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function(result) {
              if (root.props.newMess) {
                location.reload();
              }
              root.props.onChange(JSON.parse(result).sender);

            },
            error: function(result) {}
        });
    }(root));
}

// upload image
var UploadImageInbox = React.createClass({
    renderFormUpload: function() {
        var stylebtnCancel = {
            marginLeft: '5px'
        };
        var root = this;
        return (
            React.createElement('div', {},
                React.createElement('p', {}, 'Please choose a file to upload. JPG, PNG, GIF only'),
                React.createElement('div', {
                        className: 'form-group'
                    },
                    React.createElement('label', {
                        'for': 'file'
                    }, 'File input'),
                    React.createElement('input', {
                        'accept': "image/*",
                        className: 'form-control',
                        type: 'file',
                        id: 'file-mess'
                    })
                ),
                React.createElement('a', {
                    onClick: function() {
                        var urlReplyMess = root.props.data.urlReplyMess;
                        var file = jQuery('#file-mess')[0].files[0];
                        if (file) {
                            var formData = new FormData();
                            formData.append('act', 'img');
                            formData.append('file', file);
                            if (root.props.newMess){
                              formData.append('id', JSON.stringify({
                                  idSender: root.props.data.profile.id,
                                  idReceiver: jQuery('#user-select').val()
                              }));
                            }
                            else {
                              formData.append('id', JSON.stringify({
                                  idSender: root.props.data.profile.id,
                                  idReceiver: root.props.messShow.idSender
                              }));
                            }
                            (function(root) {
                                jQuery.ajax({
                                    type: "post",
                                    dataType: 'json',
                                    url: urlReplyMess,
                                    data: formData,
                                    cache: false,
                                    processData: false,
                                    contentType: false,
                                    success: function(result) {
                                        if (root.props.newMess) {
                                          location.reload();
                                        }
                                        root.props.onChange(JSON.parse(result).sender);
                                    },
                                    error: function(result) {}
                                });
                            }(root));
                        }
                    },
                    className: 'btn btn-success btn-sm'
                }, 'Upload'),
                React.createElement('a', {
                    style: stylebtnCancel,
                    'data-dismiss': "modal",
                    className: 'btn btn-default btn-sm'
                }, 'Cancel')
            )
        );
    },
    render: function() {
        var styleh4 = {
            fontSize: '18px',
            fontWeight: '300'
        };
        return (
            React.createElement('div', {},
                React.createElement('div', {
                        className: 'modal fade',
                        role: 'dialog',
                        id: 'uploadImageMess'
                    },
                    React.createElement('div', {
                            className: 'modal-dialog'
                        },
                        React.createElement('div', {
                                className: 'modal-content'
                            },
                            React.createElement('div', {
                                    className: 'modal-header',
                                    style: {
                                        padding: '20px 30px'
                                    }
                                },
                                React.createElement('button', {
                                    className: 'close',
                                    type: 'button',
                                    'data-dismiss': 'modal',
                                    'aria-hidden': 'true'
                                }, 'x'),
                                React.createElement('h4', {
                                    style: styleh4,
                                    className: "modal-title"
                                }, 'Upload image')
                            ),
                            React.createElement('div', {
                                    className: 'modal-body',
                                    style: {
                                        padding: '20px 30px'
                                    }
                                },
                                this.renderFormUpload()
                            )
                        )
                    )
                )
            )
        );
    }
});
var UploadLinkVideo = React.createClass({
    renderFormSendVideo: function() {
        var stylebtnCancel = {
            marginLeft: '5px'
        };
        var root = this;
        return (
            React.createElement('div', {},
                React.createElement('p', {}, 'Paste link video ember to send'),
                React.createElement('div', {
                        className: 'form-group'
                    },
                    React.createElement('input', {
                        className: 'form-control',
                        type: 'text',
                        id: 'text-link'
                    })
                ),
                React.createElement('a', {
                    onClick: function() {
                        var urlReplyMess = root.props.data.urlReplyMess;
                        var link = jQuery('#text-link').val();
                        if (link != '') {
                            var formData = new FormData();
                            formData.append('act', 'video');
                            formData.append('link', link);
                            if (root.props.newMess){
                              formData.append('id', JSON.stringify({
                                  idSender: root.props.data.profile.id,
                                  idReceiver: jQuery('#user-select').val()
                              }));
                            }
                            else {
                              formData.append('id', JSON.stringify({
                                  idSender: root.props.data.profile.id,
                                  idReceiver: root.props.messShow.idSender
                              }));
                            }
                            (function(root) {
                                jQuery.ajax({
                                    type: "post",
                                    dataType: 'json',
                                    url: urlReplyMess,
                                    data: formData,
                                    cache: false,
                                    processData: false,
                                    contentType: false,
                                    success: function(result) {
                                        if (root.props.newMess) {
                                          location.reload();
                                        }
                                        root.props.onChange(JSON.parse(result).sender);
                                    },
                                    error: function(result) {}
                                });
                            }(root));
                        }
                    },
                    className: 'btn btn-success btn-sm'
                }, 'Send'),
                React.createElement('a', {
                    style: stylebtnCancel,
                    'data-dismiss': "modal",
                    className: 'btn btn-default btn-sm'
                }, 'Cancel')
            )
        );
    },
    render: function() {
        var styleh4 = {
            fontSize: '18px',
            fontWeight: '300'
        };
        return (
            React.createElement('div', {},
                React.createElement('div', {
                        className: 'modal fade',
                        role: 'dialog',
                        id: 'sendVideo'
                    },
                    React.createElement('div', {
                            className: 'modal-dialog'
                        },
                        React.createElement('div', {
                                className: 'modal-content'
                            },
                            React.createElement('div', {
                                    className: 'modal-header',
                                    style: {
                                        padding: '20px 30px'
                                    }
                                },
                                React.createElement('button', {
                                    className: 'close',
                                    type: 'button',
                                    'data-dismiss': 'modal',
                                    'aria-hidden': 'true'
                                }, 'x'),
                                React.createElement('h4', {
                                    style: styleh4,
                                    className: "modal-title"
                                }, 'Send video')
                            ),
                            React.createElement('div', {
                                    className: 'modal-body',
                                    style: {
                                        padding: '20px 30px'
                                    }
                                },
                                this.renderFormSendVideo()
                            )
                        )
                    )
                )
            )
        );
    }
});
