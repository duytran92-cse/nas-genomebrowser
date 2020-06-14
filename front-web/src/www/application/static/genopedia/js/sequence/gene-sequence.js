var GeneSequence = React.createClass({
    getInitialState: function () {
      var url = this.props.data[0].url_api;
      var data = [];
      if(this.props.data[0].data.length == 0){
        data = {
              chromosome: '1',
              end: 9999,
              start: 0,
              exon: [],
              gene: [],
              id: 0,
              name: '',
            }
      }
      else {
        data = JSON.parse(this.props.data[0].data);
      }
        return {
            geneSequence: data,
            url: url
        }
    },
    componentWillMount(){
      this.handleBlockUI();
    },
    componentDidMount: function() {
       gene = this.getURLParameter('gene');

       this.handleLoadData(gene);
   },
    handleBlockUI: function() {
        var root = this;
        jQuery("#sequence-browser-gene").block({
               message: "<img src='/img/loading.gif' />",
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
     getURLParameter:function(variable) {
       var gene = decodeURI(window.location.pathname).split("/").pop()
    //    var vars = query.split("&");
    //    for (var i=0;i<vars.length;i++) {
    //        var pair = vars[i].split("=");
    //        if(pair[0] == variable){return pair[1];}
    //    }
        return gene;
        // return(false);
    },
    handleLoadData: function(gene){
        var _this = this;
        var url = this.state.url + '/gene/get';

        jQuery.ajax({
             type: "get",
             dataType: 'json',
             crossDomain: true,
             url: url,
             data: {
                 'gene': gene
             },
             async: false,
             success: function (result) {
                 if (result['status'] == 'ok') {
                   _this.setState({
                     geneSequence: result['data']['record']
                   });
                   jQuery("#sequence-browser-gene").unblock();

                 }
             },
             error: function (result) {
             }
         });
    },
    renderExonPointer: function (data) {
        var elements = [];
        var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];

        ////////////////////////////////////////////////////////////////////////////
        var pointerIndicate = 0;
        var index = 0;
        var root = this;
        ///////////////////////////////////
        var start = Math.ceil(data.start / 20);
        var end = Math.ceil(data.end / 20);

        // exons
        pointer_exon = []
        if (data.exon) {
          for (var i = 0; i < data.exon.length; i++) {
              _start = Math.ceil(data.exon[i].start / 20);
              _end = Math.ceil(data.exon[i].end / 20);
              for (var j = _start; j <= _end; j++) {
                  pointer_exon.push(j)
              }
          }
        }

        // genes
        pointer_gene = []
        exonName = {}
        var eleTooltipParent = {}
        if (data.gene) {
          for (var i = 0; i < data.gene.length; i++) {
              _start = Math.ceil(data.gene[i].start / 20);
              _end = Math.ceil(data.gene[i].end / 20);
              for (var j = _start; j <= _end; j++) {
                  if ( jQuery.inArray( j, pointer_exon ) == -1 ) {
                      pointer_gene.push(j)
                  }
              }

              // exon name
              eN = 1;
              for (var e = 0; e < data.gene[i].exon.length; e++) {
                key = Math.ceil(data.gene[i].exon[e].start / 20);
                exonName[key] = 'Exon ' + eN;
                eN = eN + 1;
                var eleTooltip = [];
                eleTooltip.push(
                    React.createElement('p', {}, 'Chromosome: '+ data.chromosome),
                    React.createElement('p', {}, 'Position ['+ data.gene[i].exon[e].start+ "-"+ data.gene[i].exon[e].end+"]"),
                    React.createElement('p', {}, 'Gene: '+ data.gene[i].name),
                    React.createElement('p', {}, 'Num variation: '+ data.gene[i].exon[e].num_variation)
                );
                var eleTooltip = '';
                eleTooltip = 'Chromosome: '+ data.chromosome + "\n"+ 'Position ['+ data.gene[i].exon[e].start+ "-"+ data.gene[i].exon[e].end+"]" + "\n" + 'Gene: '+ data.gene[i].name+ "\n"+ 'Num variation: '+ data.gene[i].exon[e].num_variation;
                eleTooltipParent[key] = eleTooltip;
              }
          }
        }

        for (var i = start ; i <= end; i++) {
            var attrGeneWrapper = {};
            var attr = {};
            attr.className = 'exon-pointer pointer';
            attrGeneWrapper.className = 'gene-wrapper';

            if (jQuery.inArray( i, pointer_exon ) !== -1) {
                attrGeneWrapper.className += ' gene-wrapper-color';
                attr.className += ' icon-Gen'+mapping[pointerIndicate%6] + ' light';
                if (i in exonName) {
                  element = React.createElement('div', {},
                                React.createElement('div', {
                                    style: {'cursor': 'pointer'},
                                    className: 'labelName',
                                    'data-toggle': 'tooltip',
                                    'data-placement': 'bottom',
                                    'data-html': 'true',
                                    'title': eleTooltipParent[i]
                                    },
                                    exonName[i]
                                ),
                                React.createElement('div', attr)
                            )
                }else element = React.createElement('div', attr);


            }else if (jQuery.inArray( i, pointer_gene ) !== -1) {
                attrGeneWrapper.className += ' gene-wrapper-color';
                attr.className += ' icon-Gen'+mapping[pointerIndicate%6] + ' gray';
                element = React.createElement('div', attr);
            }else{
                attr.className += ' icon-Gen'+mapping[pointerIndicate%6] + ' gray';
                element = React.createElement('div', attr);
            }

            elements.push(
                React.createElement('div', {key: pointerIndicate, className: 'exon-sequence'},
                    React.createElement('div', attrGeneWrapper,
                        element
                    )
                )
              );
            pointerIndicate = pointerIndicate + 1;
        }
        ///////////////////////////////////
        return elements;
    },
    handleAjaxLoadExonSequence:function(pos) {

       if ( pos > 0 ) {
           var start = this.state.geneSequence.end + 1;
       }
       var chromosome= this.state.geneSequence.chromosome;
       var parent = this;

       var rs = [];
       var url = this.state.url+ '/gene/load/' + chromosome+'/'+start;
       jQuery.ajax({
           type: "get",
           dataType: 'json',
           url: url,
           async: false,
           success: function (result) {
                if (result['status'] == 'ok') {
                    rs = result['data']['record'];
                }
           }
        });
        if (rs['start'] && rs['end']) {
            _current_state = this.state.geneSequence;
            var min = Math.min(_current_state.start, rs['start']);
            var max = Math.max(_current_state.end, rs['end']);
            _current_state.start = min;
            _current_state.end = max;
            this.setState({geneSequence: _current_state});
        }

    },
    renderGeneName: function(data){
      elements = [];
      stage = 0;
      k = 0;
      if (data.gene) {
        c_start = Math.ceil(data.start / 20);
        for (var i = 0; i < data.gene.length; i++) {
            _start = Math.ceil(data.gene[i].start / 20);
            margin = Math.ceil(((data.gene[i].start - data.start) *5))/ 20;
            margin_left = (margin - stage - k*30) + 'px';
            stage = margin;
            k = k + 1;
            elements.push(
              React.createElement('span', {className: 'topName', style: {'marginLeft': margin_left}}, data.gene[i].name)
            );
        }
      }
      return elements;
    },
    handleMoveNext: function() {
        var distance = $('.exon-sequence:last').offset().left - $('.exon-bar').offset().left - 450;
        if (distance <= $('.exon-bar').width()) {
            this.handleAjaxLoadExonSequence(1000);
        }
        var leftPos = $('.exon-bar').scrollLeft()+450;
        $(".exon-bar").stop().animate({scrollLeft: leftPos }, 400);
    },
    handleMoveBack: function() {
       var leftPos = $('.exon-bar').scrollLeft();
       $(".exon-bar").stop().animate({scrollLeft: leftPos - 450}, 400);
    },
    renderControlPanel: function () {
      return (
        React.createElement('div', {className: 'sequenceControlBtnGroup'},
          React.createElement('div', {className: 'rightGroup'},
            React.createElement('div', {className: 'viewlevel'}, 'Magnification level: Gene'),
            React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-chevron-left', onClick: this.handleMoveBack }),
           React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-chevron-right', onClick: this.handleMoveNext })
          )
        )
      );
    },
    render: function(){
        return (
            React.createElement('div', {className: 'row'},
               React.createElement('div', {className: 'inner_con_banner'},
                   React.createElement('div', {},
                       React.createElement('div', {className: 'exon-bar-top exon-bar'},
                           React.createElement('div', {className: 'sequenceGenesName'}, this.renderGeneName(this.state.geneSequence)),
                           React.createElement('div', {className: 'exon-pointer-top'},this.renderExonPointer(this.state.geneSequence))
                       ),
                       React.createElement('div', {style: {height: '15px'}}, ''

                       ),
                       React.createElement('div', {className: 'exon-bar-bottom exon-bar'},
                           React.createElement('div', {className: 'exon-pointer-top'}, this.renderExonPointer(this.state.geneSequence))
                       ),
                       this.renderControlPanel()
                   )
               )

           )

        );
    }
});
