var Variations = React.createClass({
    getInitialState: function() {
        console.log(this.props.data);
        return ({
            variations:     this.props.data.variations,
            totalPage:      this.props.data.totalPage,
            currentPage:    this.props.data.currentPage,
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
        jQuery(document).ready(function(){
            $('[data-toggle="popover"]').popover({ html : true });   
        });
    },
    changePage: function(page) {                
        document.location = '/variations?page=' + page;
    },
    justifyAlphabetList: function () {
        var div = document.getElementById('variations-list');
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
        jQuery("#variations-list").block({
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
/*
    RENDER
*/    
    render_404: function() {
        return (
            React.createElement('div', {}, 
                React.createElement('h2', {className: "lead text-center"}, "Not found")
            )
        );
    },
    renderItem: function () {        
        var ele = [];
        var styleItem = {margin: '10px', backgroundColor: 'gray', height: '100px', width: '100px'};
        var stylespan = {minWidth: '18%', display: 'inline-block', 'fontSize': '16px'};
        var i = 0;
        var eleTemp = [];
        var itemLength = this.state.variations.length - 1;

        this.state.variations.map(function (item, key) {
            var diseaseComponent = (typeof item.disease != 'undefined') ? this.renderDisease(item.disease) : "";
            var publicationComponent = (typeof item.publication != 'undefined') ? this.renderPublication(item.publication) : "";
            var geneComponent = (typeof item.gene != 'undefined') ? this.renderGene(item.gene) : "";

            i++;
            eleTemp.push(React.createElement('li', {},
                React.createElement('a', {key: key, href: '/variation/'+item.rsnumber},
                    React.createElement('span', {style: stylespan}, "» "+item.rsnumber),
                    geneComponent,
                    diseaseComponent,
                    publicationComponent
                )
            ));
            if (i == 50 || key == itemLength) {
                i = 0;
                ele.push(
                    React.createElement('ul', {className: 'listData_ul'}, eleTemp)
                );
                eleTemp = [];
            }
        }.bind(this));
        return ele;
    },    
    renderDisease: function(disease) {
        var content = '';
        disease.map(function(item, key) {
            content = '<li>'+'<a href="/disease/'+item+'">'+item+'</a>'+'</li>'
        });
        content = '<ul>'+content+'</ul>';
        return (React.createElement('a', {'data-toggle':'popover', 'data-placement': 'bottom', 'data-content': content, className: "gene-exinfo"}, 'disease'));
    },
    renderPublication: function(publication) {
        var content = '';
        publication.map(function(item, key) {
            content = '<li>'+'<a href="http://www.ncbi.nlm.nih.gov/pubmed/'+item.pmid+'" target="_blank">'+item.title+'</a>'+'</li>'
        });
        content = '<ul>'+content+'</ul>';
        return (React.createElement('a', {'data-toggle':'popover', 'data-placement': 'bottom', 'data-content': content, className: "gene-exinfo"}, 'publication'));
    },
    renderGene: function(gene) {
        var content = '';
        content = '<li>'+'<a href="/gene/'+gene+'" target="_blank">'+gene+'</a>'+'</li>'
        content = '<ul>'+content+'</ul>';
        return (React.createElement('a', {'data-toggle':'popover', 'data-placement': 'bottom', 'data-content': content, className: "gene-exinfo"}, 'gene'));
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
                React.createElement('ul', {className: 'pagination pagination-sm pagination-list '},
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
                this.renderItem()
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
        if ((this.state.variations != null) && (this.state.variations.length > 0)) {
            content = this.render_content();
        } else {
            content = this.render_404();
        }

        return (
            React.createElement('div', {className: "row", style: {"minHeight": "500px"}}, 
                React.createElement('div', {className: "col-md-12 col-sm-12"},
                    content
                )
            )
        )
    }
});
