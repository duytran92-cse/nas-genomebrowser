var LabOfferComponent = React.createClass({
  getInitialState: function() {
    return (
      {
        offerList: [],
        offers: [],
        totalPage:  0,
        pageNow: 0,
        labUser:[],
      }
    );
  },
  componentWillMount: function() {
    this.handleBlockUI();
  },
  componentDidUpdate: function() {
      this.handleBlockUI();
  },
  componentDidMount: function() {
    this.handleLoadData({});
  },
  ///////////////////////////////////////////////////////////////////////////////
  // METHOD
  handleBlockUI: function() {
    var root = this;
    $("#offerListBlock").block({
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
  handleLoadData: function(sendData) {
    root = this;
    sendData['token'] = getCookie('token');
    jQuery.ajax({
      url:LAB_NETWORK_API+'/api/loadLabUserOffer',
      data:sendData,
      method:'GET',
    }).done(function(result){
      if (result['code'] ==100) {
        jQuery(".notfound-div").html(result['error']);
      } else if(result['code'] ==200) {
        data = result['data'];
        var offerList = data.dataRows;
        root.setState({offerList: offerList, totalPage: data.totalPage, pageNow: data.pageNow, offers: []});
        jQuery("#offerListBlock").unblock();
      }
    });
  },
  handleSearchOffers: function(keyword) {
    this.handleLoadData({keyword: keyword});
  },
  changePageVariation: function(page) {
    this.handleLoadData({page: page});
  },

  ///////////////////////////////////////////////////////////////////////////////
  // RENDER
  render: function() {
    
    return (
      React.createElement('div', {className: 'container-fluid'},
        React.createElement('div', {className: 'row'},
          React.createElement('div', {className: 'col-md-12'},
            React.createElement(HeadComponent, {
              handleSearchOffers: this.handleSearchOffers,
              handleLoadLabUser: this.handleLoadLabUser,
            })
          ),
          React.createElement('div', {id: 'offerListBlock',className: 'col-md-12'},
            React.createElement(BodyComponent, {
              offerList: this.state.offerList,
              offers: this.state.offers,
              groupOffers: this.state.groupOffers,
              pageNow: this.state.pageNow,
              totalPage: this.state.totalPage,
              changePageVariation: this.changePageVariation,
              handleEditOffer: this.handleEditOffer
            })
          )
        )
      )
    );
  }
});

var HeadComponent = React.createClass({
  propTypes: {
    handleSearchOffers: React.PropTypes.func,
    handleLoadLabUser:React.PropTypes.func,
    labUser:React.PropTypes.array,
  },

  ///////////////////////////////////////////////////////////////////////////////
  // RENDER
  render: function() {
    var root = this;
    return (
      React.createElement('div', {className: 'row', style: {marginBottom: '20px'}},
        React.createElement('div', {className: 'col-md-12 col-sm-12', style: { marginTop: '6px'}},
          React.createElement('div', {className: 'pull-left'},
            React.createElement('a', {
                className: 'btn-s-green clickable',
                'data-toggle':"modal",
                'data-target':"#offerForm",
                onClick:function(){
                    jQuery('#offerForm').modal('show');
                    jQuery('#offerForm #idOffer').val('').trigger('change');
                }
              },
              "Add new offer"),
            React.createElement('a', {
                className: 'btn-s-blue clickable',
                href:"/labQuestionList"
              },
              "View offer questions")
          ),
          React.createElement('div', {className: 'pull-right'},
            React.createElement(UserComponent)
          )
        )
      )
    );
  }
});
var BodyComponent = React.createClass({
  propTypes: {
		offerList: React.PropTypes.array,
    changePageVariation: React.PropTypes.func,
    handleEditOffer: React.PropTypes.func,
    handlChangeAlphabet: React.PropTypes.func
  },  
  componentDidMount: function() {
    var root = this;
    jQuery('#offerListReloadElement').change(function() {
      root.changePageVariation(root.props.pageNow);
    });
  },

  handleOnEditClick: function(idOffer) {
    jQuery('#offerForm').modal('show');
    jQuery('#offerForm #idOffer').val(idOffer).trigger('change');
  },
  handleOnDeleteClick: function(idOffer) {
    if (confirm("Are you sure to delete?")) {
      var root = this;
      sendData = {};
      sendData['token'] = getCookie('token');
      sendData['idOffer'] = idOffer;
      jQuery.ajax({
        url:LAB_NETWORK_API+'/api/offerDelete',
        data:sendData,
        method:'GET',
      }).done(function(result){
        if (result['code'] ==100) {
          jQuery(".notfound-div").html(result['error']);
        } else if(result['code'] ==200) {
          jQuery('#offerListReloadElement').trigger('change');
        }
      });
    }
  },
  handleVOnBackClick: function() {
    jQuery("#offer-list-div").toggle('600');
    jQuery("#offer-result-list-div").toggle('600');
  },
  handleOfferSearchID: function(idOffer) {
    var ele = document.getElementById('aq-idOffer');
    ele.value = idOffer;
  },
  handleScrollSection: function(event) {
    event.preventDefault();
    // Calculate destination place
    var dest=0;
    if(event.target.offsetTop > jQuery(document).height()-jQuery(window).height()){
         dest=jQuery(document).height()-jQuery(window).height();
    }else{
         dest=event.target.offsetTop;
    }
    // Go to destination
    jQuery('html,body').animate({scrollTop:dest}, 1000, 'swing');
  },

  changePageVariation: function(page) {
    this.props.changePageVariation(page);
  },

  renderOfferBox: function() {
      var found = React.createElement('div', {className: 'tab-content'},
        React.createElement('div', {id: 'home', className: 'tab-pane fade in active'},
          React.createElement('div', {id: 'offer-list-div'},
          
            React.createElement('div', {className: 'offerListResult'},
              React.createElement('table', {className: 'table table-striped table-hover table-offerSearch'},
                React.createElement('thead', {className: 'header'},
                  React.createElement('tr', {},
                    React.createElement('th', {}, 'ID Offer'),
                    React.createElement('th', {}, 'Laboratory Code'),
                    React.createElement('th', {}, 'Price'),
                    React.createElement('th', {}, 'Action')
                  )
                ),
                React.createElement('tbody', {},
                  this.renderOfferBoxItem()
                )
              )
            ),
            this.renderPaging()
          )
        )
      );
      var notFound = React.createElement('div', {className: 'notfound-div'}, "Not found");
      return (this.props.offerList.length > 0) ? found : notFound;
  },

  renderOfferBoxItem: function() {
    var items = [];
    var root = this;
    this.props.offerList.map(function(i, k) {
      var editAttr = {};
      editAttr.className = "clickable fa fa-pencil";
      editAttr.onClick = root.handleOnEditClick.bind(null, i.id);

      var deleteAttr = {};
      deleteAttr.className = "clickable fa fa-trash";
      deleteAttr.style ={'marginLeft':10};
      deleteAttr.onClick = root.handleOnDeleteClick.bind(null, i.id);
      
      var item = React.createElement('tr', {key: k},
        React.createElement('td', {}, i.id),
        React.createElement('td', {}, i.labCode),
        React.createElement('td', {}, i.price),
        React.createElement('td', {},
          React.createElement('a', editAttr),
          React.createElement('a', deleteAttr)
        )
      );
      items.push(item);
    });

    return items;
  },
  
  renderOfferLabItem: function() {
    var items = [];
    var root = this;
    this.props.offerList.map(function(i, k) {
      var viewAttr = {};
      viewAttr.className = 'scroll clickable  fa fa-search fa-search-left';
      viewAttr.onClick = root.handleScrollSection;
      var item =
        React.createElement('tr', {key: k},
          React.createElement('td', {}, i.diseaseName),
          React.createElement('td', {}, i.geneName),
          React.createElement('td', {}, ""),
          React.createElement('td', {},
            React.createElement('a', viewAttr)
          )
        );
      items.push(item);
    });

    return items;
  },

  
  renderPage: function () {
    var root = this;
    var pNow = this.props.pageNow;
    var limit = ((pNow+4) <= this.props.totalPage) ? (pNow+4) : this.props.totalPage;
    var i= (pNow-2 > 0) ? (pNow-2) : 1;
    if (pNow - 3 > 0) {
        if (this.props.totalPage - pNow === 1) i = pNow - 3;
    }
    if (pNow - 4 > 0) {
        if (this.props.totalPage - pNow === 0) i = pNow - 4;
    }
    var ele = [];
    var key = 0;
    for(; i<= limit; i++) {
        key++;
        if (key > 5)
            break;
        ele.push(
            React.createElement('li', {
                    id: 'page-' + i, onClick: function (e) {
                        var pClickNow = parseInt(jQuery(e.target).text());
                        root.changePageVariation(pClickNow);
                    }, className: (i == pNow) ? 'active' : ''
                },
                React.createElement('span', {}, i)
            )
        );
    }
    return ele;
  },
  renderPaging: function() {
    var root = this;
    return (
      React.createElement('div', {className: 'pull-right'},
          React.createElement('ul', {className: 'pagination pagination-xs pull-left'},
              React.createElement('li', {
                      onClick: function () {
                          root.changePageVariation(1);
                      }
                  },
                  React.createElement('span', {}, '<<')
              ),
              React.createElement('li', {
                      onClick: function () {
                          if (parseInt(root.props.pageNow) > 1) {
                              root.changePageVariation(parseInt(parseInt(root.props.pageNow)) - 1);
                          }
                      }
                  },
                  React.createElement('span', {}, '<')
              ),
              this.renderPage(),
              React.createElement('li', {
                      onClick: function () {
                          if (parseInt(root.props.pageNow) < parseInt(root.props.totalPage)) {
                            root.changePageVariation(parseInt(parseInt(root.props.pageNow)) + 1);
                          }
                      }
                  },
                  React.createElement('span', {}, '>')
              ),
              React.createElement('li', {
                      onClick: function () {
                        root.changePageVariation(parseInt(root.props.totalPage));
                      }
                  },
                  React.createElement('span', {}, '>>')
              )
          )
      )
    );
  }, // update later
  render: function() {
    return (
      React.createElement('div', {id: 'offer-result-list'},
        this.renderOfferBox()
      )
    );
  }
});


