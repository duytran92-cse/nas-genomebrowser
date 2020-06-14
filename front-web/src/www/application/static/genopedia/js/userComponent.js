var UserSection = React.createClass({
  getInitialState: function() {
      var data = this.props.data;
      return (
      {
          user: {
              idUser: data.idUser,
              fullname: data.fullname,
              position: data.position,
              about: data.about,
              age: data.age,
              gender: data.gender,
              genderText: data.genderText,
              country: data.country,
              education: data.education,
              work: data.work,
              listAchievement: data.achievements,
              imageAchievement: data.achievementsImage,
              photo: data.imageUser,
              listImage: data.listImage,
              rankPlace: 13,
              rankMedal: data.ranks,
              accountBank: {'balance': 133, 'incomming': 66, 'sum': 67},
              accountPaypal: '',
              updateUrl: data.updateUrl,
              forumPosts: data.forumPosts,
              lastPosts: [
                  {
                      idPost: 1,
                      content: 'Lorem ipsum dolor sit amet consetetur sadipscing elitr?',
                      postedAt: '20 minutes ago'
                  },
                  {
                      idPost: 2,
                      content: 'Lorem ipsum dolor zero?',
                      postedAt: '1 minutes ago'
                  },
                  {
                      idPost: 1,
                      content: 'Lorem ipsum dolor sit dow?',
                      postedAt: '10 minutes ago'
                  }],
              message: data.messages,
              statistics: {
                  'totalEntry': 233,
                  'totalEarn': 243,
                  'totalPost': 533,
                  'totalViewAllTime': 5231,
                  'totalViewInmonths': 1233
              }
          }
      }
      );
  },
  render: function() {
    return (
      React.createElement('div', {className: 'main_cont'},
        React.createElement('div', {className: 'container'},
          React.createElement('div', {className: 'row'},
            React.createElement('div', {className: 'bg_clor'},
              React.createElement('div', {className: 'seperate_line hidden'}),
              React.createElement('div', {className: 'col-md-9 col-sm-9 profile_left'},
                React.createElement(LeftComponent, {user: this.state.user})
              ),
              React.createElement('div', {className: 'col-md-3 col-sm-3 profile_right'},
                React.createElement(RightComponent, {user: this.state.user})
              ),
              React.createElement('div', {className: 'clearfix'})
            )
          )
        )
      )
    );
  }
});
// React.createElement('div', {className: ''})
var LeftComponent = React.createClass({
  propTypes: function() {
    user: React.propTypes.object
  },
  renderPhoto: function() {
      var data = this.props.user;
      var styleDelete = {cursor: 'pointer'};
      return (
          React.createElement('div', {},
              React.createElement('a', {href: '#'},
                  React.createElement('img', {src: data.photo})
              ),
              React.createElement('a', {
                      'data-toggle': 'modal',
                      'data-target': '#uploadM',
                      href: '',
                      'role': 'button',
                      className: 'buttn_left'
                  },
                  React.createElement('i', {className: 'fa fa-camera'}),
                  '\t \tUpload Photo'
              ),
              React.createElement('p', {className: 'semibold_txt small_txt m_top05 m_bot05'}, 'Maximum size of 800kb, JPG, PNG.'),
              React.createElement('p', {className: 'semibold_txt'},
                  React.createElement('a', {
                      onClick: function () {
                          var updateUrl = data.updateUrl;
                          var formData = new FormData();
                          formData.append('act', 'delete');
                          formData.append('idUser', data.idUser);
                          jQuery.ajax({
                              type: "post",
                              dataType: 'json',
                              url: updateUrl,
                              data: formData,
                              cache: false,
                              processData: false,
                              contentType: false,
                              success: function (result) {
                                  location.reload();
                              },
                              error: function (result) {
                              }
                          });
                      }, style: styleDelete, className: 'delete_link'
                  }, 'Delete this image')
              )
          )
      );
  },
  renderRankItem: function() {
    var elements = [];
    this.props.user.rankMedal.map(function(item, k) {
      var attr = {};
      attr.className = (item.isActive) ? 'selected' : '';
      var element =
        React.createElement('li', attr,
          React.createElement('img', {src: item.image}),
          React.createElement('span', {}, item.text)
        );

      elements.push(element);
    });

    return elements;
  },
  renderRank: function() {
    return (
      React.createElement('div', {className: 'rank_secs'},
        React.createElement('h1', {}),
        React.createElement('ul', {className: 'rank_details'},
          this.renderRankItem()
        ),
        React.createElement('div', {className: 'clearfix'})
      )
    );
  },
  renderInfo: function() {
      var data = this.props.user;
      var styleAbout = {height:'45px', color: '#000000'};
      var styletext  = {minHeight: '45px'};
      return (
          React.createElement('div', {},
              React.createElement('h1', {className: 'm_bot10'}, this.props.user.fullname),
              React.createElement('p', {className: 'semibold_txt'}, '(' + this.props.user.position + ')'),
              React.createElement('p', {className: 'bold_txt edit_txt'},
                  React.createElement('span', {}, 'About you'),
                  React.createElement('a', {
                          id: 'about-edit',
                          className: 'right', title: 'Edit', onClick: function (e) {
                              jQuery('#about-user').removeClass('hidden');
                              jQuery('#about-text').addClass('hidden');
                              jQuery('#about-edit').addClass('hidden');
                              jQuery('#about-save').removeClass('hidden');
                              jQuery('#about-cancel').removeClass('hidden');
                          }
                      },
                      React.createElement('i', {className: 'fa fa-pencil'})
                  ),
                  React.createElement('a', {
                          id: 'about-cancel',
                          className: 'right hidden about-cancel', title: 'Cancel', onClick: function (e) {
                              jQuery('#about-user').addClass('hidden');
                              jQuery('#about-edit').removeClass('hidden');
                              jQuery('#about-save').addClass('hidden');
                              jQuery('#about-cancel').addClass('hidden');
                              jQuery('#about-text').removeClass('hidden').text(jQuery('#about-user').val());
                          }
                      },
                      React.createElement('i', {className: 'fa fa-remove'})
                  ),
                  React.createElement('a', {
                          id: 'about-save',
                          className: 'right hidden', title: 'Save', onClick: function (e) {
                              jQuery('#about-user').addClass('hidden');
                              jQuery('#about-edit').removeClass('hidden');
                              jQuery('#about-save').addClass('hidden');
                              jQuery('#about-cancel').addClass('hidden');
                              jQuery('#about-text').removeClass('hidden').text(jQuery('#about-user').val());
                              var formData = new FormData();
                              formData.append('act', 'about');
                              formData.append('idUser', data.idUser);
                              formData.append('about', jQuery('#about-user').val());
                              var updateUrl = data.updateUrl;
                              jQuery.ajax({
                                  type: "post",
                                  dataType: 'json',
                                  url: updateUrl,
                                  data: formData,
                                  cache: false,
                                  processData: false,
                                  contentType: false,
                                  success: function (result) {
                                  },
                                  error: function (result) {
                                  }
                              });
                          }
                      },
                      React.createElement('i', {className: 'fa fa-check'})
                  )
              ),
              React.createElement('textarea', {
                  id: 'about-user',
                  style: styleAbout,
                  className: 'form-control hidden',
                  defaultValue: this.props.user.about
              }),
              React.createElement('p', {id: 'about-text', style: styletext}, this.props.user.about)
          )
      );
  },
  renderPersonalInfo: function () {
      var styleInfo = {border: 'none', color: '#000000', outline: 'none', boxShadow: 'none', appearance: 'none', paddingTop: '5px', height: '18px'};
      var styleCol1 = {'width': '30px', paddingTop: '5px', height: '18px'};
      var styleCol2 = {'width': '110px', paddingTop: '5px', height: '18px'};
      var styleCol3 = {paddingTop: '5px', height: '18px'};
      var data = this.props.user;
      return (
          React.createElement('div', {},
              React.createElement('p', {className: 'bold_txt edit_txt'}, 'Personal information ',
                  React.createElement('a', {
                          id: 'person-edit',
                          className: 'right', title: 'Edit', onClick: function (e) {
                              jQuery('#person-edit').addClass('hidden');
                              jQuery('#person-save').removeClass('hidden');
                              jQuery('#person-cancel').removeClass('hidden');
                              ////////////
                              jQuery('#gender-text').addClass('hidden');
                              jQuery('#gender-select').removeClass('hidden');
                              jQuery('#table-person input').attr('style', '').attr('readOnly', false);
                          }
                      },
                      React.createElement('i', {className: 'fa fa-pencil'})
                  ),
                  React.createElement('a', {
                          id: 'person-cancel',
                          className: 'right hidden about-cancel', title: 'Cancel', onClick: function (e) {
                              jQuery('#person-edit').removeClass('hidden');
                              jQuery('#person-save').addClass('hidden');
                              jQuery('#person-cancel').addClass('hidden');
                              ///////////////////////
                              jQuery('#gender-text').removeClass('hidden').val(jQuery('#gender-select option:selected').text());
                              jQuery('#gender-select').addClass('hidden');
                              jQuery('#table-person input').attr('style', 'color: #000000; border: none;outline: none;box-shadow: none;appearance: none; height:18px').attr('readOnly', true);

                          }
                      },
                      React.createElement('i', {className: 'fa fa-remove'})
                  ),
                  React.createElement('a', {
                          id: 'person-save',
                          className: 'right hidden', title: 'Save', onClick: function (e) {
                              jQuery('#person-edit').removeClass('hidden');
                              jQuery('#person-save').addClass('hidden');
                              jQuery('#person-cancel').addClass('hidden');
                              ///////////////////////
                              jQuery('#gender-text').removeClass('hidden').val(jQuery('#gender-select option:selected').text());
                              jQuery('#gender-select').addClass('hidden');
                              jQuery('#table-person input').attr('style', 'color: #000000; border: none;outline: none;box-shadow: none;appearance: none; height:18px').attr('readOnly', true);
                          ///////////////
                          // update profile
                          var info = {
                                'idUser'    : data.idUser,
                                'age'       : jQuery('#person-age').val(),
                                'gender'    : jQuery('#gender-select').val(),
                                'country'   : jQuery('#person-country').val(),
                                'education' : jQuery('#person-education').val(),
                                'work'      : jQuery('#person-work').val()
                          };
                          var formData = new FormData();
                          formData.append('act', 'person');
                          formData.append('data', JSON.stringify(info));
                              var updateUrl = data.updateUrl;
                              jQuery.ajax({
                                  type: "post",
                                  dataType: 'json',
                                  url: updateUrl,
                                  data: formData,
                                  cache: false,
                                  processData: false,
                                  contentType: false,
                                  success: function (result) {
                                  },
                                  error: function (result) {
                                  }
                              });
                          }
                      },
                      React.createElement('i', {className: 'fa fa-check'})
                  )
              ),
              React.createElement('div', {className: 'personaldetails_list'},
                  React.createElement('table', {id: 'table-person', className: 'table'},
                      React.createElement('tbody', {},
                          React.createElement('tr', {},
                              React.createElement('td', {style:styleCol1},
                                  React.createElement('i', {className: 'fa fa-gift'})
                              ),
                              React.createElement('td', {style: styleCol2},
                                  React.createElement('span', {}, 'Age')
                              ),
                              React.createElement('td', {style: styleCol3},
                                React.createElement('input', {id:'person-age', style: styleInfo, className: 'form-control', type: 'text', defaultValue: this.props.user.age, readOnly: 'readonly'})
                              )
                          ),
                          React.createElement('tr', {},
                              React.createElement('td', {style:styleCol1},
                                  React.createElement('i', {className: 'fa fa-mars'})
                              ),
                              React.createElement('td', {style:styleCol2},
                                  React.createElement('span', {}, 'Gender')
                              ),
                              React.createElement('td', {style:styleCol3},
                                  React.createElement('input', {id:'gender-text', type:'text', style:styleInfo, className: 'form-control', defaultValue: this.props.user.genderText, readOnly: 'readonly'}),
                                  React.createElement('select', {id:'gender-select', defaultValue: this.props.user.gender,className: 'form-control hidden'},
                                      React.createElement('option', {value: 1}, 'Male'),
                                      React.createElement('option', {value: 2}, 'Female')
                                  )
                              )
                          ),
                          React.createElement('tr', {},
                              React.createElement('td', {style:styleCol1},
                                  React.createElement('i', {className: 'fa fa-globe'})
                              ),
                              React.createElement('td', {style:styleCol2},
                                  React.createElement('span', {}, 'Country')
                              ),
                              React.createElement('td', {style:styleCol3},
                                  React.createElement('input', {id:'person-country', type:'text', style:styleInfo, className: 'form-control', defaultValue: this.props.user.country, readOnly: 'readonly'})
                              )
                          ),
                          React.createElement('tr', {},
                              React.createElement('td', {style:styleCol1},
                                  React.createElement('i', {className: 'fa fa-graduation-cap'})
                              ),
                              React.createElement('td', {style:styleCol2},
                                  React.createElement('span', {}, 'Education')
                              ),
                              React.createElement('td', {style:styleCol3},
                                  React.createElement('input', {id:'person-education', type:'text', style:styleInfo, className: 'form-control', defaultValue: this.props.user.education, readOnly: 'readonly'})
                              )
                          ),
                          React.createElement('tr', {},
                              React.createElement('td', {style:styleCol1},
                                  React.createElement('i', {className: 'fa fa-suitcase'})
                              ),
                              React.createElement('td', {style:styleCol2},
                                  React.createElement('span', {}, 'Work')
                              ),
                              React.createElement('td', {style:styleCol3},
                                  React.createElement('input', {id:'person-work', type:'text', style:styleInfo, className: 'form-control', defaultValue: this.props.user.work, readOnly: 'readonly'})
                              )
                          ),
                          React.createElement('tr', {},
                              React.createElement('td', {style:styleCol1},
                                  React.createElement('i', {className: 'fa fa-newspaper-o'})
                              ),
                              React.createElement('td', {style:styleCol2},
                                  React.createElement('span', {}, 'Forum posts')
                              ),
                              React.createElement('td', {style:styleCol3},
                                  React.createElement('input', {id:'forum-post', type:'text', style:styleInfo, className: 'form-control', defaultValue: this.props.user.forumPosts, readOnly: 'readonly'})
                              )
                          )
                      )
                  )
              )
          )
      );
  },
  renderStatistics: function() {
    return (
      React.createElement('div', {className: 'statis_ul'},
        React.createElement('h1', {className: 'border_bot'}, 'Statistics'),
        React.createElement('table', {className: 'table table-striped'},
          React.createElement('tbody', {},
            React.createElement('tr', {},
              React.createElement('td', {},
                React.createElement('i', {className: 'fa fa-file-text-o'})
              ),
              React.createElement('td', {},
                React.createElement('span', {}, this.props.user.statistics.totalEntry)
              )
            ),
            React.createElement('tr', {},
              React.createElement('td', {},
                React.createElement('i', {className: 'fa fa-euro'})
              ),
              React.createElement('td', {},
                React.createElement('span', {}, this.props.user.statistics.totalEarn)
              )
            ),
            React.createElement('tr', {},
              React.createElement('td', {},
                React.createElement('i', {className: 'fa fa-comment-o'})
              ),
              React.createElement('td', {},
                React.createElement('span', {}, this.props.user.statistics.totalPost)
              )
            ),
            React.createElement('tr', {},
              React.createElement('td', {},
                React.createElement('i', {className: 'fa fa-eye'})
              ),
              React.createElement('td', {},
                React.createElement('span', {}, this.props.user.statistics.totalViewAllTime)
              )
            ),
            React.createElement('tr', {},
              React.createElement('td', {},
                React.createElement('i', {className: 'fa fa-eye'})
              ),
              React.createElement('td', {},
                React.createElement('span', {}, this.props.user.statistics.totalViewInmonths)
              )
            )
          )
        )
      )
    );
  },
  renderAchievement: function() {
      var eleLeft = [];
      var eleRight = [];
      var styleImageLi = {
          backgroundImage: 'url('+this.props.user.imageAchievement+')',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: '0 0'
      };
      
      // Check user have any achivement. If not -> dont show achivement list
      var checkActive = false;
      listAchievement = this.props.user.listAchievement
      for (litem in listAchievement) {
          if (listAchievement[litem].isActive) {
              var checkActive = true;
          }
      }
      if (!checkActive) {
         return false;
      }
      
      this.props.user.listAchievement.map(function (item, key) {
          var attr = {};
          attr.className = (item.isActive) ? '' : 'disabled_t';
          attr.style = styleImageLi;
          if (key <= 4) {
              eleLeft.push(
                  React.createElement('li', attr,
                      React.createElement('a', {href: '#'}, item.text)
                  )
              );
          }
          else {
              eleRight.push(
                  React.createElement('li', attr,
                      React.createElement('a', {href: '#'}, item.text)
                  )
              );
          }
      });
      var styleRow= { minHeight:'230px'}
      return (
          React.createElement('div', {},
              React.createElement('h1', {className: 'border_bot'}, 'Achievements'),
              React.createElement('div', {className: 'row', style: styleRow},
                  React.createElement('div', {className: 'col-md-6 col-sm-6 achievements_secs'},
                      React.createElement('ul', {className: 'achievements_ul'}, eleLeft)
                  ),
                  React.createElement('div', {className: 'col-md-6 col-sm-6 achievements_secs'},
                      React.createElement('ul', {className: 'achievements_ul'}, eleRight)
                  )
              )
          )
      );
  },
  renderLastPost: function() {
      return (
          React.createElement('div', {},
              React.createElement('h1', {className: 'border_bot'}, 'Last forum posts'),
              this.renderLastPostItem()
          )
      );
  },
  renderLastPostItem: function() {
    var elements = [];
    this.props.user.lastPosts.map(function(item, k) {
      var element =
        React.createElement('div', {className: 'forum_post_list'},
          React.createElement('ul', {},
            React.createElement('li', {},
              React.createElement('a', {href: '#'})
            ),
            React.createElement('li', {},
              React.createElement('p', {},
                React.createElement('a', {href: '#'}, item.content)
              ),
              React.createElement('p', {className: 'tyml_txt'}, item.postedAt)
            )
          ),
          React.createElement('div', {className: 'clearfix'})
        );

      elements.push(element);
    });

    return elements;
  },
  render: function() {
    return (
      React.createElement('div', {className: 'row'},
        React.createElement('div', {className: 'col-md-3 col-sm-3 profile_left_s'},
          this.renderPhoto(),
          this.renderRank()
        ),
        React.createElement('div', {className: 'col-md-9 col-sm-9 profile_right_s'},
          this.renderInfo(),
          this.renderPersonalInfo(),
        //   this.renderStatistics(), => statistic
          React.createElement('div', {className: 'clearfix'}),
          this.renderAchievement()
        //   this.renderLastPost()
        ),
        React.createElement('div', {className: 'clearfix'})
      )
    );
  }
});

var RightComponent = React.createClass({
  propTypes: function() {
    user: React.propTypes.object
  },
  renderAccountBank: function() {
      var styleUserMenu = { paddingRight: '10px' };
      var styleMenu     = { backgroundColor: '#FFFFFF'};
      return (
          React.createElement('div', {className: 'right_p_bg'},
              React.createElement('h1', {style: styleMenu}, React.createElement('i', {style: styleUserMenu, className: 'fa fa-bars'}), 'User Menu'),
              React.createElement('ul', {},
                  React.createElement('li', {},
                      React.createElement('span', {}, 'Account balance: '),
                      React.createElement('span', {}, this.props.user.accountBank.balance)
                  ),
                  React.createElement('li', {},
                      React.createElement('span', {}, 'Waiting for verification: '),
                      React.createElement('span', {}, this.props.user.accountBank.incomming)
                  ),
                  React.createElement('li', {},
                      React.createElement('span', {}, 'Sum available: '),
                      React.createElement('span', {}, this.props.user.accountBank.sum)
                  )
              ),
              React.createElement('div', {className: 'clearfix'})
          )
      );
  },
  renderAccountPaypal: function() {
      var styleMoney = { backgroundColor: '#FFFFFF'};
      return (
          React.createElement('div', {className: 'right_p_bg'},
              React.createElement('h2', {style: styleMoney}, 'Withdraw Money'),
              React.createElement('div', {className: 'right_p_bg2'},
                  React.createElement('img', {src: this.props.user.listImage.paypal}),
                  React.createElement('p', {className: 'text-center semibold_txt m_top10'},'Commission: ',
                      React.createElement('span', {}, '2%')
                  ),
                  React.createElement('p', {className: 'text-center semibold_txt m_top10'},'Currency: ',
                      React.createElement('span', {}, 'EURO')
                  ),
                  React.createElement('a', {className: 'buttn', href: '#'}, 'Transfer sum now')
              )
          )
      );
  },
  renderProfile: function() {
      var styleProfile = {backgroundColor: '#FFFFFF'};
      var styleStatic = {paddingLeft: '10px'};
      return (
          React.createElement('div', {className: 'right_p_bg'},
              React.createElement('h2', {style: styleProfile}, 'Profile'),
              React.createElement('div', {className: 'right_p_bg'},
                  React.createElement('ul', {},
                      React.createElement('li', {className: 'semibold_txt'},
                          React.createElement('a', {href: '#'},
                              React.createElement('i', {className: 'fa fa-globe'}),
                              React.createElement('span', {style: styleStatic}, 'Statistics public')
                          )
                      ),
                      React.createElement('li', {className: 'semibold_txt'},
                          React.createElement('a', {href: '#'},
                              React.createElement('i', {className: 'fa fa-lock'}),
                              React.createElement('span', {style: styleStatic}, 'Statistics private')
                          )
                      )
                  )
              ),
              React.createElement('div', {className: 'right_p_bg2'},
                  React.createElement('a', {href: '#'},
                      React.createElement('img', {src: this.props.user.listImage.fb})
                  )
              )
          )
      );
  },
  renderMessage: function() {
      var styleMessage = { paddingRight: '10px'};
      var styleInbox = { backgroundColor: '#FFFFFF'};
      return (
          React.createElement('div', {className: 'right_p_bg'},
              React.createElement('h2', {style: styleInbox}, 'Inbox'),
              this.renderMessageItem(),
              React.createElement('div', {className: 'right_p_bg2'},
                  React.createElement('a', {className: 'buttn',style: styleInbox, href: '/inbox'},
                      React.createElement('i', {style: styleMessage, className: 'fa fa-envelope'}), 'Message'),
                  React.createElement('div', {className: 'clearfix gap'}),
                  React.createElement('ul', {},
                      React.createElement('li', {className: 'clear-hover-li'},
                          React.createElement('a', {
                              'data-toggle': 'modal',
                              'data-target': '#deleteAlert',
                              href: '',
                              'role': 'button',
                          }, 'Delete Account')
                    //       ,
                    //   React.createElement('a', {}, '|'),
                    //   React.createElement('a', {href: '#'}, 'Contact Support')
                  )
              ),
              React.createElement(AlertDelete, {})
          )
      )
      );
  },
  renderMessageItem: function() {
      var elements = [];
      var styleMessage = {cursor: 'text'};
      var styleName    = {cursor: 'pointer'};
      this.props.user.message.map(function (item, k) {
          elements.push(
              React.createElement('div', {className: 'right_p_bg3'},
                  React.createElement('ul', {},
                      React.createElement('li', {className: 'clear-hover-li'},
                          React.createElement('p', {className: 'semibold_txt'},
                              React.createElement('a', {herf: '#'},
                                  React.createElement('img', {src: item.image})
                              )
                          )
                      ),
                      React.createElement('li', {className: 'clear-hover-li'},
                          React.createElement('div', {},
                              React.createElement('a', {style: styleName, className: 'semibold_txt', href: '#'}, item.name),
                              React.createElement('p', {style: styleMessage}, item.message)
                          )
                      )
                  ),
                  React.createElement('div', {className: 'clearfix'})
              )
          )
      });
      return elements;
  },
  render: function() {
    return (
      React.createElement('div', {},
        // this.renderAccountBank(), account
        // this.renderAccountPaypal(),
        // this.renderProfile(),
        this.renderMessage()
      )
    );
  }
});

var UploadImageProfile = React.createClass({
    renderFormUpload: function() {
        var stylebtnCancel = {marginLeft: '5px'};
        var data = this.props.data;
        return (
            React.createElement('div', {},
                React.createElement('p', {}, 'Please choose a file to upload. JPG, PNG, GIF only'),
                React.createElement('div', {className: 'form-group'},
                    React.createElement('label', {'htmlFor': 'file-profile'}, 'File input'),
                    React.createElement('input', {
                        'accept': "image/jpg, image/pnd, image/jpeg",
                        className: 'form-control',
                        type: 'file',
                        id: 'file-profile'
                    })
                ),
                React.createElement('a', {
                    onClick: function () {
                        var updateUrl = data.updateUrl;
                        var file = jQuery('#file-profile')[0].files[0];
                        if (file) {
                            var formData = new FormData();
                            formData.append('act', 'img');
                            formData.append('file', file);
                            formData.append('idUser', data.idUser);
                            jQuery.ajax({
                                type: "post",
                                dataType: 'json',
                                url: updateUrl,
                                data: formData,
                                cache: false,
                                processData: false,
                                contentType: false,
                                success: function (result) {
                                    location.reload();
                                },
                                error: function (result) {
                                }
                            });
                        }
                    }, className: 'btn btn-success btn-sm'
                }, 'Save'),
                React.createElement('a', {
                    style: stylebtnCancel,
                    'data-dismiss': "modal",
                    className: 'btn btn-default btn-sm'
                }, 'Cancel')
            )
        );
    },
    render: function() {
        var styleh4 = { fontSize: '18px', fontWeight: '300'};
        return (
            React.createElement('div', {},
                React.createElement('div', {className: 'modal fade', role: 'dialog', id: 'uploadM'},
                    React.createElement('div', {className: 'modal-dialog'},
                        React.createElement('div', {className: 'modal-content'},
                            React.createElement('div', {className: 'modal-header', style: {padding: '20px 30px'} },
                                React.createElement('button', {className: 'close', type: 'button', 'data-dismiss': 'modal', 'aria-hidden': 'true'}, 'x'),
                                React.createElement('h4', {style: styleh4, className: "modal-title"},'Upload new avatar')
                            ),
                            React.createElement('div', {className: 'modal-body', style: {padding: '20px 30px'}},
                                this.renderFormUpload()
                            )
                        )
                    )
                )
            )
        );
    }
});



var AlertDelete = React.createClass({
    renderFormAlert: function() {
        var stylebtnCancel = {marginLeft: '5px'};
        var data = this.props.data;
        return (
            React.createElement('div', {},
                React.createElement('a', {
                    onClick: function () {
                            jQuery.ajax({
                                type: "post",
                                dataType: 'json',
                                url: '/api/deleteAccount',
                                data: '',
                                cache: false,
                                processData: false,
                                contentType: false,
                                success: function (result) {
                                    location.href = '/';
                                },
                                error: function (result) {
                                }
                            });
                        }
                    , className: 'btn btn-success btn-sm'
                }, 'Ok'),
                React.createElement('a', {
                    style: stylebtnCancel,
                    'data-dismiss': "modal",
                    className: 'btn btn-default btn-sm'
                }, 'Cancel')
            )
        );
    },
    render: function() {
        var styleh4 = { fontSize: '18px', fontWeight: '300'};
        return (
            React.createElement('div', {},
                React.createElement('div', {className: 'modal fade', role: 'dialog', id: 'deleteAlert'},
                    React.createElement('div', {className: 'modal-dialog'},
                        React.createElement('div', {className: 'modal-content'},
                            React.createElement('div', {className: 'modal-header', style: {padding: '20px 30px'} },
                                React.createElement('button', {className: 'close', type: 'button', 'data-dismiss': 'modal', 'aria-hidden': 'true'}, 'x'),
                                React.createElement('h4', {style: styleh4, className: "modal-title"},'Are you sure delete this account ?')
                            ),
                            React.createElement('div', {className: 'modal-body', style: {padding: '20px 30px'}},
                                this.renderFormAlert()
                            )
                        )
                    )
                )
            )
        );
    }
});
