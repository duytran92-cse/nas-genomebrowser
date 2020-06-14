var Diseases = React.createClass({
    getInitialState: function() {        
        return ({
            diseases:       this.props.data.diseases,
            totalPage:      this.props.data.totalPage,
            currentPage:    this.props.data.currentPage,
            currentLetter:  this.props.data.letter
        });
    }, 
/*
    METHOD
*/  
    componentWillUpdate: function() {
        this.handleBlockUI();
    },
    componentWillMount: function() {
        this.handleBlockUI();
    },
    componentDidMount: function () {
        this.justifyAlphabetList();
        this.handlAlphabetActive(this.state.currentLetter);
        window.addEventListener('resize', this.justifyAlphabetList);

        jQuery(document).ready(function(){
            $('[data-toggle="popover"]').popover({ html : true });   
        });
    },
    changePage: function(page) {                
        document.location = '/diseases?page=' + page + '&' + 'lt=' + this.state.currentLetter.toUpperCase();
    },
    justifyAlphabetList: function () {
        var div = document.getElementById('diseases-list');
        var availableLen = parseInt(div.offsetWidth);
        var itemLen = parseInt(Math.floor(availableLen / 27));

        var lis = document.getElementsByClassName('alphabets');
        for(var i = 0; i < lis.length; i++)
        {
          var width = (itemLen-2)+'px';
          lis[i].style.width = width;
        }
    },
    handleBlockUI: function() {        
        var root = this;
        jQuery("#diseases-list").block({
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
    handlChangeAlphabet: function(letter) {            
        document.location = '/diseases?page=1&' + 'lt=' + letter.toUpperCase();
    },
    handlAlphabetActive: function(letter) {        
       jQuery('.alphabets').removeClass('letter-active');
       jQuery('#alphabets-disease-'+letter).addClass('letter-active');
    },

/*
    RENDER
*/    
    renderAlphabetItem: function() {
        var alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
        var items = [];
        var root = this;
        alphabets.map(function(i, k) {
          var itemAttr = {};
          itemAttr.className = "alphabets-letter";
          itemAttr.onClick = root.handlChangeAlphabet.bind(null, i);

          var liAttr = {};
          liAttr.key = k;
          liAttr.className = (k === 0) ? 'alphabets letter-active' : 'alphabets';
          liAttr.id = 'alphabets-disease-'+i;          
          var item =
            React.createElement('li', liAttr,
              React.createElement('a', itemAttr, i.toUpperCase())
            );

          items.push(item);
        });
        return items;
    },
    render_404: function() {
        return (
            React.createElement('div', {}, 
                React.createElement('h2', {className: "lead text-center"}, "Not found")
            )
        );
    },
    renderItem: function () {
        var styleItem = {margin: '10px', backgroundColor: 'gray', height: '100px', width: '100px'};
        var stylespan = {width: '40%', display: 'inline', 'fontSize': '17px'};
        var eleTemp = [];
        var itemLength = this.state.diseases.length - 1;

        this.state.diseases.map(function (item, key) {            
            var geneComponent = (typeof item.gene != 'undefined') ? this.renderGene(item.gene) : "";
            var publicationComponent = (typeof item.publication != 'undefined') ? this.renderPublication(item.publication) : "";

            eleTemp.push(React.createElement('li', {},
                React.createElement('a', {key: key, href: '/disease/'+item.name},
                    React.createElement('span', {style: stylespan}, "» "+item.name),
                    geneComponent,
                    publicationComponent
                )
            ));
        }.bind(this));
        return eleTemp;
    },    
    renderGene: function(gene) {
        var content = '';
        gene.map(function(item, key) {
            content = '<li>'+'<a href="gene/'+item+'" target="_blank">'+item+'</a>'+'</li>'
        });
        content = '<ul>'+content+'</ul>';
        return (React.createElement('a', {'data-toggle':'popover', 'data-placement': 'bottom', 'data-content': content, className: "gene-exinfo"}, 'gene'));
    },
    renderPublication: function(publication) {
        var content = '';
        publication.map(function(item, key) {
            content = '<li>'+'<a href="http://www.ncbi.nlm.nih.gov/pubmed/'+item.pmid+'" target="_blank">'+item.pmid+'</a>'+'</li>'
        });
        content = '<ul>'+content+'</ul>';
        return (React.createElement('a', {'data-toggle':'popover', 'data-placement': 'bottom', 'data-content': content, className: "gene-exinfo"}, 'publication'));
    },
    renderPagingItem: function () {
        var state = this.state;
        var root = this;
        var pNow = state.currentPage;
        var limit = ((pNow+4) <= state.totalPage) ? (pNow+4) : state.totalPage;
        var i= (pNow-2 > 0) ? (pNow-2) : 1;
        if (pNow - 3 > 0) {
            if (state.totalPage - pNow == 1) i = pNow - 3;
        }
        if (pNow - 4 > 0) {
            if (state.totalPage - pNow == 0) i = pNow - 4;
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
                            root.changePage(pClickNow);
                        }, className: (i == pNow) ? 'active' : ''
                    },
                    React.createElement('span', {}, i)
                )
            )
        }
        return ele;
    },
    renderPagination: function() {
        var root = this;
        return (
            React.createElement('div', {className: 'text-center'},
                React.createElement('ul', {className: 'pagination pagination-sm pagination-list'},
                    React.createElement('li', {
                            onClick: function () {
                                root.changePage(1);
                            }
                        },
                        React.createElement('span', {}, '<<')
                    ),
                    React.createElement('li', {
                            onClick: function () {
                                if (parseInt(root.state.currentPage) > 1) {
                                    root.changePage(parseInt(parseInt(root.state.currentPage)) - 1);
                                }
                            }
                        },
                        React.createElement('span', {}, '<')
                    ),
                    this.renderPagingItem(),
                    React.createElement('li', {
                            onClick: function () {
                                if (parseInt(root.state.currentPage) < parseInt(root.state.totalPage)) {
                                    root.changePage(parseInt(parseInt(root.state.currentPage)) + 1);
                                }
                            }
                        },
                        React.createElement('span', {}, '>')
                    ),
                    React.createElement('li', {
                            onClick: function () {
                                root.changePage(parseInt(root.state.totalPage));
                            }
                        },
                        React.createElement('span', {}, '>>')
                    )
                )
            )
        );
    },
    render_content: function() {        
        return React.createElement('div', {className: 'row'},
            React.createElement('div', {className: 'col-md-12 col-sm-12'},
                React.createElement('ul', {style: {'width': "100%"}, className: 'listData_ul'}, 
                    this.renderItem()
                )
            ),
            React.createElement('div', {className: 'col-md-12 col-sm-12'},
                this.renderPagination()
            )
        );
    },
    render:function () {
        var styleInput = {width: '50px', height: '20px'};
        var styledivPar = {display: 'inline'};
        var styleul = {display: 'inline-flex'};
        
        var content = null;
        if ((this.state.diseases != null) && (this.state.diseases.length > 0)) {
            content = this.render_content();
        } else {
            content = this.render_404();
        }

        return (
            React.createElement('div', {className: "row", style: {"minHeight": "500px"}}, 
                React.createElement('div', {className: "col-md-12 col-sm-12"},
                    React.createElement('ul', {className: 'nav nav-tabs', style: {"margin": "15px 0"}},
                      this.renderAlphabetItem()
                    ),
                    content
                )
            )
        )
    }
});
