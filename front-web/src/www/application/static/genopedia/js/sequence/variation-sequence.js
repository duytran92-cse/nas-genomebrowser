var VariationSequence = React.createClass({
 getInitialState: function () {
  var url = this.props.data[0].url_api;
  var datain = [];
  if(this.props.data[0].data.length == 0){
    datain = {
        parameters: {
          chromosome: '1',
          start: 956700,
          end: 956900,
          position: 0,
          rsnumber: '',
        },
        variation: [
          {
            chromosome :"1",
            gene: "",
            id: 1,
            position: 99999,
            rsnumber:'',
          }
        ],
        sequence:'CAGGAGGAGCAACGTGTTGTCACTTGCGCTGAAGAAGGCTCCAAGCGTCCCCTGCGTGGAGAACAGCCCCTCCCACCAGCACAGCCTCAGGCGCCTCAGGTGAGGCAAGGCCAGATCTCTGCCTGGGCACCCAGCTGCCCGCCCCTCGCTGCTGCTCACCTCAGGTGAGGCAAGGCCAGATTTCTGCCTGGGCACCCAGCTGCCCGCCCCTGGCTGCTGCTCACCTTTGC'
    }
  }
  else {
      datain = JSON.parse(this.props.data[0].data);
  }
  this.props.data = datain;

  return {
     data: datain,
     url_api: url,
     rsnumber: ''
   }
 },

 componentWillMount(){
   this.handleBlockUI();
 },
 componentDidMount: function() {
     rsnumber = this.getURLParameter('rsnumber');
     this.handleLoadData(rsnumber);
   },
 handleBlockUI: function() {
        var root = this;
        jQuery("#sequence-browser-variation").block({
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
      var rsnumber = decodeURI(window.location.pathname).split("/").pop()
   //    var vars = query.split("&");
   //    for (var i=0;i<vars.length;i++) {
   //        var pair = vars[i].split("=");
   //        if(pair[0] == variable){return pair[1];}
   //    }
       return rsnumber;
       // return(false);
 },
 handleLoadData: function(rsnumber){
   var _this = this;
   var _url = this.state.url_api + '/sequences/get';
   _this.setState({
       rsnumber: rsnumber
   });
   jQuery.ajax({
        type: "get",
        dataType: 'json',
        crossDomain: true,
        url : _url,
	      async: false,
        data : {
          'rsnumber': rsnumber
        },
        success: function (result) {
            if (result['status'] == 'ok') {
              _this.setState({
                      data: result['data']['record'],
                    });
              jQuery("#sequence-browser-variation").unblock();
          }
        },
        error: function (result) {
        }
    });
 },
 renderSequencePointer: function (variables) {
    var styleText = {height: '33px', 'marginTop': '-33px', 'fontWeight': 'bold','position':'absolute', 'cursor': 'pointer'};
    var elements = [];
    if (variables) {
        if (variables.sequence != '') {
          var mappingLetter = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'};
          var str = variables.sequence;
          var stringTop = str!=null ? str.split(""):[];
          var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];
          var index = 0;
          var data = this.handlePosition(variables.parameters);

          var exonStart = data[0];
          var exonEnd = data[1];
          var snpPosition = data[2];

          var variation = variables.variation;

          for(i = data[0]; i < data[1]; i++){
            var letterTop = stringTop[index];
            var letterBottom = mappingLetter[letterTop];
            var root = this;

            var attrBehind = {};
            attrBehind.key = i;
            attrBehind.className = i;

            var attrLetterAbove = {};
            attrLetterAbove.className = 'letter';

            var attrLetterBottom = {};
            attrLetterBottom.className = 'letter letter-gray';

            var attrSequence = {};
            attrSequence.key = i;
            attrSequence.className = 'sequence';

            var attr = {};
            attr.key = i;
            attr.className = 'snp-pointer';
            attr.className = attr.className + ' icon-Gen'+mapping[i%6];

            element = React.createElement('div', {},
                          React.createElement('div', {style: styleText}, rs),
                          React.createElement('div', attr)
                      )

            element = React.createElement('div', attr);
            // Exon
            if (i >= exonStart && i <= exonEnd) {
                attr.className = attr.className +' pointer-hightlight';
                element = React.createElement('div', attr);

                for (j = 0; j < variation.length; j++) {

                    var eleTooltip = '';
                    eleTooltip = 'Chromosome: '+ variation[j]['chromosome'] + "\n"+ 'Position: '+ variation[j]['position'] + "\n" + 'Gene: '+ variation[j]['gene']+ "\n"+ 'Associated diseases:'+ variation[j]['associated_disease'];

                    var j_position = Math.floor(variation[j]['position'] - variables.parameters.start);
                    if (j_position == i && snpPosition == i) {
                        var color = ' snp-mutation-hightlight ';
                        attr.className = attr.className + color + ' variation-pointer';
                        attrLetterAbove.className = attrLetterAbove.className + ' letter-mutation';
                        var rs = variation[j]['rsnumber'];
                        // element = React.createElement('div', attr);
                        element = React.createElement('div', {},
                                        React.createElement('div', {
                                                style: styleText,
                                                className: 'dropdown',
                                                'data-toggle': 'tooltip',
                                                'data-placement': 'bottom',
                                                'data-html': 'true',
                                                'title': eleTooltip
                                            },
                                            rs
                                        ),
                                        React.createElement('div', attr)
                                  )
                        break;
                    }else if (j_position == i) {
                        var color = ' snp-mutation-hightlight-bonus ';
                        attr.className = attr.className + color + ' variation-pointer';
                        attrLetterAbove.className = attrLetterAbove.className + ' letter-mutation-bonus';
                        var rs = variation[j]['rsnumber'];
                        // element = React.createElement('div', attr);
                        element = React.createElement('div', {},
                                        React.createElement('div', {
                                                style: styleText,
                                                className: 'dropdown',
                                                'data-toggle': 'tooltip',
                                                'data-placement': 'bottom',
                                                'data-html': 'true',
                                                'title': eleTooltip
                                            },
                                            rs
                                        ),
                                        React.createElement('div', attr)
                                  )
                        break;
                    }
                }
             } //----for
             elements.push(
               React.createElement('div', attrSequence,
                 React.createElement('div', attrBehind,
                   React.createElement('div', attrLetterAbove, letterTop),
                   element,
                   React.createElement('div', attrLetterBottom, letterBottom)
                 )
               )
             );
             index++;
          }
        }
    }
    return elements;
 },
 handlePosition: function(exon) {
   var terminal = Math.floor(exon.end - exon.start);
   var exonStart = 0;
   var exonEnd = terminal;
   var snpPosition = (exon.position - exon.start);

 return [exonStart, exonEnd, snpPosition];
},
handleAjaxLoadSequence:function(pos) {

  if ( pos > 0 ) {
      var start = this.state.data.parameters.end + 1;
      var end = start + 200;
  } else {
      var end = this.state.data.parameters.start - 1;
      var start = end - 200;
  }

  var parent = this;
  var rs = [];
  rsnumber = this.state.rsnumber;
  var _url = this.state.url_api+'/sequences/load/' + rsnumber + '/' + start + '/' + end;
  $.ajax({
      type: "GET",
       dataType: 'json',
       url: _url,
       async: false,
      success: function (result) {
          if (result['status'] == 'ok') {
              rs = result['data']['record'];
          }
      },
      error: function (result) {

      }
   });
  _current_state = this.state.data;
  var min = Math.min(_current_state.parameters.start, rs['parameters']['start']); //bug here
  var max = Math.max(_current_state.parameters.end, rs['parameters']['end']);
  _current_state.parameters.start = min;
  _current_state.parameters.end = max;
  if (pos > 0 ) { // next
      _current_state.variation = rs['variation'].concat(_current_state.variation);
      _current_state.sequence += rs['sequence'];

  }else{ // previous
      _current_state.variation = (_current_state.variation).concat(rs['variation']);
      _current_state.sequence = rs['sequence'] + _current_state.sequence;
  }
    this.setState({data: _current_state});
},
handleMoveNext: function() {
 var distance = $('.sequence:last').offset().left - $('.variation-bar').offset().left - 450;
 if (distance <= $('.variation-bar').width()) {
   this.handleAjaxLoadSequence(1000);
 }
 var leftPos = $('.variation-bar').scrollLeft()+450;
 $(".variation-bar").stop().animate({scrollLeft: leftPos }, 400);
},
handleMoveBack: function() {
//  this.handleAjaxLoadSequence(-1000);
var leftPos = $('.variation-bar').scrollLeft();
$(".variation-bar").stop().animate({scrollLeft: leftPos - 450}, 400);

},
renderControlPanel: function () {
 return (
   React.createElement('div', {className: 'sequenceControlBtnGroup'},
     React.createElement('div', {className: 'rightGroup'},
       React.createElement('div', {className: 'viewlevel'}, 'Magnification level: Sequence'),
       React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-chevron-left', onClick: this.handleMoveBack }),
                React.createElement('span', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-chevron-right', onClick: this.handleMoveNext })
     )
   )
 );
},
renderSequenceLevel: function(){
   return (
     React.createElement('div', {className: 'inner_con_banner'},
        React.createElement('div', {id: 'sequence-panel'},
          // Variation bar
          React.createElement('div', {className: 'variation-bar-top variation-bar'},
            // Pointer bar top
            React.createElement('div', {className: 'variation-pointer-top'},

                this.renderSequencePointer(this.state.data)
            ) //----------variation-pointer-top----
          ),
          React.createElement('div', {style: {height: '35px'}}, ''

          ),
          React.createElement('div', {className: 'variation-bar-bottom variation-bar'},
            // Pointer bar top
            React.createElement('div', {className: 'variation-pointer-top'},
                this.renderSequencePointer(this.state.data)
            ) //----------variation-pointer-top----
          ),
            // Control pannel
            this.renderControlPanel()
        ) // --sequence-panel---
     ) // -----inner_con_banner---
   )
 },
 render: function() {
    return (
      React.createElement('div', {className: 'row'},
      React.createElement('div', {className: 'images_secs'}, this.renderSequenceLevel())
     )
    )
  }
});
