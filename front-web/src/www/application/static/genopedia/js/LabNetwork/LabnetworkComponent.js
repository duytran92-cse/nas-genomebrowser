var LabnetworkComponent = React.createClass({
  getInitialState: function() {
    return (
      {
        offerSearchs: [],
        offers: [],
        groupOffers: [],
        totalPage:  0,
        pageNow: 0,
        currentLetter:'0',
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
		$("#offerSearchsBlock").block({
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
      this.serverRequest = jQuery.post(LAB_NETWORK_API+'/api/loadOffer', JSON.stringify(sendData), function (result) {
      var data = JSON.parse(result);
      var os = data.dataRows;
      this.setState({offerSearchs: os, totalPage: data.totalPage, pageNow: data.pageNow, offers: []});
      jQuery("#offerSearchsBlock").unblock();
    }.bind(this));
  },
  handlChangeAlphabet: function(letter) {

    this.setState({currentLetter: letter.toUpperCase()});
    this.handleLoadData({letter: letter});
  },
  handleSearchOffers: function(keyword) {
    this.handleLoadData({keyword: keyword});
  },
  changePageVariation: function(page) {
    this.handleLoadData({page: page});
  },
  handleViewlOffers: function(groupKey) {
    var offersGroupKey = {offersGroupKey: groupKey};
    this.serverRequest = jQuery.post(LAB_NETWORK_API+'/api/viewOffers', JSON.stringify(offersGroupKey),function (result) {
      var data = JSON.parse(result);
      this.setState({offers: data.offersDetail, groupOffers: data.offersGroup});
      jQuery("#offerSearchsBlock").unblock();
    }.bind(this));
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
            })
          ),
          React.createElement('div', {id: 'offerSearchsBlock',className: 'col-md-12'},
            React.createElement(BodyComponent, {
              offerSearchs: this.state.offerSearchs,
              offers: this.state.offers,
              groupOffers: this.state.groupOffers,
              pageNow: this.state.pageNow,
              totalPage: this.state.totalPage,
              currentLetter: this.state.currentLetter,
              changePageVariation: this.changePageVariation,
              handleViewlOffers: this.handleViewlOffers,
              handlChangeAlphabet: this.handlChangeAlphabet
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
  componentDidMount: function() {
    var root = this;
    $(document).on("keypress", "form#offer-search-form", function(event) { 
      if(event.keyCode == 13) {
        root.handleSearchOffers();
        return false;
      }
    });
  },
  ///////////////////////////////////////////////////////////////////////////////
  // METHOD
  handleSearchOffers: function() {
    var keyword = this.refs.keyword.value;
    if (keyword.trim() === '') {
      jQuery('#pop-emessage-search').html('Please enter keyword');
      return;
    }
    // Valid
    this.props.handleSearchOffers(keyword);
    jQuery('.alphabets').removeClass('letter-active');
    jQuery('#pop-emessage-search').html('');
    jQuery('#currentLetter').html('');
  },

  ///////////////////////////////////////////////////////////////////////////////
  // RENDER
  render: function() {
    var root = this;
    var text = "GENE BAY is an open platform for genetic testing services, connecting genetic testing service providers with clinicians requiring genetic testing. Any lab can register to offer ist services and any clinician can order from a portfolio of more than 3000 different genetic tests. Genetic testing made easy";
    
  
    return (
      React.createElement('div', {className: 'row', style: {marginBottom: '20px'}},
        React.createElement('div', {className: 'col-md-3 col-sm-3'},
          React.createElement('form', {id:'offer-search-form'},
            React.createElement('fieldset', {},
              React.createElement('span', {className: 'gene-word'}, "SEARCH"),
              React.createElement('div', {className: 'form-group', style: { marginTop: '16px'}},
                React.createElement('input', {ref: 'keyword', className: 'form-control search-box', placeholder: 'Enter keyword', id: 'search-box-text',
            
              }),
              React.createElement('span', {className: 'help-block'}, "")
              ),
              React.createElement('p', {className: 'pull-left pop-emessage', id: 'pop-emessage-search'}),
              React.createElement('a', {
                className: 'btn btn-s-green pull-right clickable',
                onClick: this.handleSearchOffers
              }, "Search")
            )
          )
        ),
        React.createElement('div', {className: 'col-md-6 col-sm-6'},
          React.createElement('div',{style: {marginBottom: '20px'} },
            React.createElement('span', {className: 'gene-word', style: {fontWeight: 'bold'}}, "GENE"),
            React.createElement('span', {className: 'bay-word', style: {fontWeight: 'bold'}}, "BAY"),
            React.createElement('p', {style: { marginTop: '10px' } }, text)
          )
        ),
        
        React.createElement('div', {className: 'col-md-3 col-sm-3 pull-right', style: { marginTop: '6px'}},
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
		offerSearchs: React.PropTypes.array,
    changePageVariation: React.PropTypes.func,
    handleViewlOffers: React.PropTypes.func,
    handlChangeAlphabet: React.PropTypes.func
	},
  componentDidMount: function () {
      this.justifyAlphabetList();
      this.handleCloseAskQuestionForm();
      window.addEventListener('resize', this.justifyAlphabetList);
  },
  handleCloseAskQuestionForm:function(){
    $('#faqM').on('hidden.bs.modal', function () {
      jQuery('#mess-res-faq').text('').attr('style', '');
      $('#askQuestionForm').trigger('reset');
    });
  },
  //////////////////////////////////////////////////////////////////////////////
  // METHOD
  handlChangeAlphabet: function(letter) {
    this.props.handlChangeAlphabet(letter);
    jQuery('#search-box-text').val('');
    // Hiden offers list
    jQuery("#offer-list-div").show('600');
    jQuery("#offer-result-list-div").hide('600');
     
  },
  handlChangeAlphabetActive: function(id) {
    jQuery('.alphabets').removeClass('letter-active');
    jQuery('#'+id).addClass('letter-active');
    jQuery('#offer-result-list-div').css('display', 'none');
  },
  handleVOnViewClick: function(groupKey) {
    jQuery("#offer-list-div").hide('600');
    this.props.handleViewlOffers(groupKey);
    jQuery("#offer-result-list-div").show('600');
  },
  handleVOnBackClick: function() {
    jQuery("#offer-list-div").show('600');
    jQuery("#offer-result-list-div").hide('600');
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
  justifyAlphabetList: function () {
    var div = document.getElementById('offer-result-list');
    var availableLen = parseInt(div.offsetWidth);
    var itemLen = parseInt(Math.floor(availableLen / 27));

    var lis = document.getElementsByClassName('alphabets');
    for(var i = 0; i < lis.length; i++)
    {
      var width = (itemLen-2)+'px'; // ' - ' margin-right
      lis[i].style.width = width;
    }
  },
  changePageVariation: function(page) {
    this.props.changePageVariation(page);
  },
  //////////////////////////////////////////////////////////////////////////////
  // RENDER
  renderAlphabetItem: function() {
    var alphabets = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    var items = [];
    var root = this;
    alphabets.map(function(i, k) {
      var itemAttr = {};
      itemAttr.className = "alphabets-letter";
      itemAttr.onClick = root.handlChangeAlphabet.bind(null, i);

      var liAttr = {};
      liAttr.key = k;
      liAttr.className = (k === 0) ? 'alphabets letter-active' : 'alphabets';
      liAttr.id = 'alphabets-'+k;
      liAttr.onClick = root.handlChangeAlphabetActive.bind(null, 'alphabets-'+k);
      var item =
        React.createElement('li', liAttr,
          React.createElement('a', itemAttr, i.toUpperCase())
        );

      items.push(item);
    });
    return items;
  },
  renderOfferBox: function() {
      var found = React.createElement('div', {className: 'tab-content'},
        React.createElement('div', {id: 'home', className: 'tab-pane fade in active'},
          React.createElement('div', {id: 'offer-list-div'},
            React.createElement('div', {className: 'pull-left'},
              React.createElement('h1', {className: 'currentLetter', id: "currentLetter"}, this.props.currentLetter)
            ),
            React.createElement('div', {className: 'pull-right offerSearchResult'},
              React.createElement('table', {className: 'table table-striped table-hover table-offerSearch'},
                React.createElement('thead', {className: 'header'},
                  React.createElement('tr', {},
                    React.createElement('th', {}, 'Disease'),
                    React.createElement('th', {}, 'Gene'),
                    React.createElement('th', {}, 'Price range'),
                    React.createElement('th', {}, 'View')
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
      return (this.props.offerSearchs.length > 0) ? found : notFound;
  },

  renderOfferBoxItem: function() {
    var items = [];
    var root = this;
    this.props.offerSearchs.map(function(i, k) {
      var viewAttr = {};
      viewAttr.className = "clickable fa fa-search fa-search-left";
      viewAttr.onClick = root.handleVOnViewClick.bind(null, i.groupKey);

      var item = React.createElement('tr', {key: k},
        React.createElement('td', {}, 
          React.createElement('a', {className: "clickable" ,onClick: root.handleVOnViewClick.bind(null, i.groupKey)}, i.diseaseName)
        ),
        React.createElement('td', {}, i.geneName),
        React.createElement('td', {}, i.priceRange),
        React.createElement('td', {},
          React.createElement('a', viewAttr)
        )
      );
      items.push(item);
    });

    return items;
  },
  renderDetailOffer: function() {
    var backAttr = {};
    backAttr.className = 'pull-right btn-back buttn btn-s-green';
    backAttr.onClick = this.handleVOnBackClick;
    var divAttr = {};
    divAttr.id = 'offer-result-list-div';
    divAttr.style = {};
    divAttr.style.display = (this.props.offers.length > 0) ? 'block' : 'none';

    return (
      React.createElement('div', divAttr,
        React.createElement('table', {className: 'table table-striped table-hover table-offerSearch'},
          React.createElement('thead', {className: 'header'},
            React.createElement('tr', {},
              React.createElement('th', {}, "Disease name"),
              React.createElement('th', {}, "Gene name"),
              React.createElement('th', {}, "Price"),
              React.createElement('th', {}, "View")
            )
          ),
          React.createElement('tbody', {},
            this.renderOfferLabItem()
          )
        ),
        React.createElement('div', {style: {marginBottom: '65px'}},
          React.createElement('h2', {className: 'pull-left number-found'}, "We found "+ this.props.offers.length +" result"),
          React.createElement('strong', backAttr, "Back")
        ),
        this.renderOfferLabDetail()
      )
    );
  },
  renderOfferLabItem: function() {
    var items = [];
    var root = this;
    this.props.groupOffers.map(function(i, k) {
      var viewAttr = {};
      viewAttr.className = 'scroll clickable  fa fa-search fa-search-left';
      viewAttr.href = '#'+i.idOffer;
      var item =
        React.createElement('tr', {key: k},
          React.createElement('td', {}, i.diseaseName),
          React.createElement('td', {}, i.geneName),
          React.createElement('td', {}, i.price),
          React.createElement('td', {},
            React.createElement('a', viewAttr)
          )
        );
      items.push(item);
    });

    return items;
  },
  handleOpenDownloadOrderForm:function(idOffer){
    var options = jQuery('select[name="pd_country"]');
    var options2 = jQuery('select[name="ref_country"]');
    var options3 = jQuery('select[name="rda_country"]');
    var options4 = jQuery('select[name="iv_country"]');
    
    var root = this;
    jQuery.get(LAB_NETWORK_API+"/api/load_regions", function(data){
      var result = JSON.parse(data);
      jQuery.each(result,function(index, item) {
        options.append('<option class="region" value=' + item.name + '>' + item.name + '</option>');
        options2.append('<option class="region" value=' + item.name + '>' + item.name + '</option>');
        options3.append('<option class="region" value=' + item.name + '>' + item.name + '</option>');
        options4.append('<option class="region" value=' + item.name + '>' + item.name + '</option>');
      });
      options.select2();
      options2.select2();
      options3.select2();
      options4.select2();
    });
    
    jQuery('#offerFormM #idOffer').val(idOffer);
    jQuery('#offerFormM').modal('show');
  },
  renderOfferLabDetail: function() {
    var items = [];
    var root = this;
    this.props.offers.map(function(i, k) {
      var item =
        React.createElement('section', {id: i.idOffer, key: k,className:'section-offer-detail'},
          React.createElement('div', {className: 'panel panel-defaul panel-result'},
            React.createElement('div', {className: 'panel-heading panel-heading-result'},
              React.createElement('strong', {}, "Offer " + (k+1))
            ),
            React.createElement('div', {className: 'panel-body'},
              React.createElement('div', {className: 'row'},
                React.createElement('div', {className: 'col-md-6 col-sm-6'},
                  React.createElement('table', {className: 'table table-striped table-hover'},
                    React.createElement('tbody', {},
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Lab code"),React.createElement('td', {}, i.labCode)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Offer number"),React.createElement('td', {}, i.idOffer)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Certification"),React.createElement('td', {}, i.cerfitication))
                    )
                  )
                ),
                React.createElement('div', {className: 'col-md-6 colsm-6'},
                  React.createElement('table', {className: 'table table-striped table-hover'},
                    React.createElement('tbody', {},
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Disease"),React.createElement('td', {}, i.disease)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Gene(s)"),React.createElement('td', {}, i.gene)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Mutation"),React.createElement('td', {}, i.mutation)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Method"),React.createElement('td', {}, i.method)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "TAT"),React.createElement('td', {}, i.tat)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Sample type"),React.createElement('td', {}, i.sampleType)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}, "Price"),React.createElement('td', {}, i.price)),
                      React.createElement('tr', {}, React.createElement('td', {className: 'text-bold-short'}),React.createElement('td', {},
                        React.createElement('div', {className: 'pull-right'},
                          React.createElement('button', {onClick: root.handleOfferSearchID.bind(null, i.idOffer), className: 'btn-s-green buttn1', 'data-toggle':"modal", 'data-target': "#faqM"}, "Ask question"),
                          React.createElement('button', {onClick: root.handleOpenDownloadOrderForm.bind(null, i.idOffer) ,className: 'buttn1 btn-s-blue'}, "Download offer")
                        )
                      )
                    )
                  )
                )
              )
            )
          )
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
        React.createElement('ul', {className: 'nav nav-tabs'},
          this.renderAlphabetItem()
        ),
        this.renderOfferBox(),
        this.renderDetailOffer()
      )
    );
  }
});
