var BannerComponent = React.createClass({
  getInitialState : function() {    
    return {
      indexLetter: 0,
      chromosome: this.props.data.chromosome,
      chromosomeHighlighter: this.props.data.chromosomeHighlight,
      chrImgSrc: this.props.chrImgSrc,
      geneSequence: {
        viewerLength: 20,
        viewerRange: [0, 116],
        chromosome: this.props.data,
        gene: this.props.data,
        exon: this.props.data.exon,
        snp: this.props.data
      }
    };
  },
  handleAjaxLoadSequence:function(pos) {

    if (pos>0 ) {
        this.state.geneSequence.exon.end += pos;
    } else {
        this.state.geneSequence.exon.start += pos;
    }

    var parent = this;
    jQuery.ajax({
      url:'/sequenceLoad',
      data:{
        start: this.state.geneSequence.exon.start,
        end:  this.state.geneSequence.exon.end,
        chromosome: this.state.geneSequence.exon.chromosome,
      }
    }).done(function(data){
        parent.state.geneSequence.exon.sequence = data.sequence;
        parent.setState(parent.state);
        // Special for prev button
        if (pos<0 ) {
            var distance = 9*pos*(-1);
            var leftPos = jQuery('.variation-bar').scrollLeft();
            jQuery(".variation-bar").animate({scrollLeft: leftPos + (distance)}, 0);

        }
    });

  },
  componentDidMount: function() {
      var root = this;
      jQuery('.potential').click(function() {
          var mappingLetter = { 'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G' };
          var potentialPair = jQuery(this).text().split('/');
          var topLetterTop = potentialPair[0];
          var topLetterBottom = mappingLetter[topLetterTop];
          var bottomLetterTop = potentialPair[1];
          var bottomLetterBottom = mappingLetter[bottomLetterTop];

          // Scroll up
          jQuery("html, body").animate({ scrollTop: 130 }, 800);

          // Fade out
          jQuery("#sequence-ex-top").fadeOut(1050);
          jQuery("#sequence-ex-bottom").fadeOut(1050);

          // Change it
          jQuery('#letter-variation-top-top').text(topLetterTop);
          jQuery('#letter-variation-top-bottom').text(topLetterBottom);
          jQuery('#letter-variation-bottom-top').text(bottomLetterTop);
          jQuery('#letter-variation-bottom-bottom').text(bottomLetterBottom);

          // Fade in
          jQuery("#sequence-ex-top").fadeIn(1100);
          jQuery("#sequence-ex-bottom").fadeIn(1100);
      });
      // $("#sequence-browser").unblock();
  },
  componentWillMount: function() {
		// this.handleBlockUI();
	},
	componentDidUpdate: function() {
		// this.handleBlockUI();
	},
	handleBlockUI: function() {
		var root = this;
		jQuery("#sequence-browser").block({
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
  handleResizeOnVariation: function(data) {
      var parentWidth = Math.floor(jQuery('.inner_con_banner').width());
      var proportion = Math.floor(parentWidth/9); // 9 is 9px, the width of a pointer
      var snpPosition = (data/proportion);
      var geneSequence = this.state.geneSequence;
      geneSequence.viewerRange[0] = (Math.floor(snpPosition) * proportion);
      geneSequence.viewerRange[1] = (Math.ceil(snpPosition) * proportion);

      this.setState({
          geneSequence: geneSequence
      });
  },
  justifyPosition: function(data=false) {
    var panel = jQuery('#sequence-panel').width();

    var left_position = parseInt(jQuery('#snpName').css('margin-left').replace('px', ''));
    var distance = Math.ceil((left_position)-(panel/2));
    var leftPos = jQuery('.variation-bar').scrollLeft();
    jQuery(".variation-bar").animate({scrollLeft: leftPos + (distance)}, 400);
  },
  sequenceLevel: function(k) {
    if (this.state.geneSequence.exon[k].hasOwnProperty('snps')) {
      if (this.state.geneSequence.exon[k].snps.length > 0) {
        var href = '/variation/'+this.state.geneSequence.exon[k].snps[0];
        window.location.href = href;
      }
    }
  },
  exonLevel: function() {
    if (this.state.geneSequence.gene.geneId !== '') {
      var href = '/gene/'+this.state.geneSequence.gene.geneId;
      window.location.href = href;
    }
  },
  render: function() {
    return (
      React.createElement('div', {className: 'images_secs'},
      React.createElement(ChromosomeComponent, {
        chromosome: this.state.chromosome
      }),
      React.createElement(ChromosomeHighlighterComponent, {
        highlighter: this.state.chromosomeHighlighter,
        chrImgSrc: this.state.chrImgSrc
      }),
        React.createElement('img', {className: 'img-chrom-body ', src: this.props.imgSrc}),
        React.createElement(SequenceBrowserComponent, {
          viewerLength: this.state.geneSequence.viewerLength,
          viewerRange: this.state.geneSequence.viewerRange,
          chromosome: this.state.geneSequence.chromosome,
          gene: this.state.geneSequence.gene,
          exon: this.state.geneSequence.exon,
          snp: this.state.geneSequence.snp,
          // Funcs
          moveNext: this.moveSequenceNext,
          moveBack: this.moveSequenceBack,
          sequenceLevel: this.sequenceLevel,
          justifyPosition: this.justifyPosition,
          handleResizeOnVariation: this.handleResizeOnVariation,
          handleAjaxLoadSequence: this.handleAjaxLoadSequence,
        })
      )
    );
  }

});
/////////////////////////////////////////
// x. CHROMOSOME COMPONENT
var ChromosomeComponent = React.createClass({
  propTypes: {
     chromosome: React.PropTypes.object
  },
  render: function() {
    var cutChromName = this.props.chromosome.chromosomeId.replace('chromosome:','');
    var genPairText = "Chromosome pair "+cutChromName;
    return (
        React.createElement('div', {className: 'div_chrom'},
          React.createElement('div', {},
            React.createElement('span', {className: 'chromName'}, genPairText),
          React.createElement('div', {className: 'chromLeft', title: "Chromosome "+cutChromName}),
          React.createElement('div', {className: 'chromRight', title: "Chromosome "+cutChromName}),
          React.createElement('div', {className: 'connector-text-genPairInfo'},
            React.createElement('p', {}, this.props.chromosome.numOfGenes + ' genes'),
            React.createElement('p', {}, this.props.chromosome.numOfSNPs + ' SNPs'),
            React.createElement('p', {}, this.props.chromosome.numOfDiseases + ' diseases')
          )
        )
      )
    );
  }
});
/////////////////////////////////////////
// x. CHROMOSOME HIGHLIGHTER COMPONENT
var ChromosomeHighlighterComponent = React.createClass({
  propTypes: {
    highlighter: React.PropTypes.object,
    chrImgSrc: React.PropTypes.string
  },
  renderItems: function() {
    var ignore = parseInt(this.props.highlighter.chromosome);
    var elements = [];
    for (var i = 1; i <= 25; i++) {
      if (i != ignore) {
        var attr = {};
        attr.className = 'chrom'+i.toString();
        attr.title = (i == 25) ? "Mitochondrial DNA" : "Chromosome " + i.toString();

        var fileImg = this.props.chrImgSrc.replace('__FILENAME__', 'c' + i.toString() + '.png');

        var element = (
          React.createElement('div', {key: i},
            React.createElement('div', attr,
              React.createElement('img', { src: fileImg, className: "img-responsive", style: {'left': '0px'} })
            )
          )
        ); // end element
        elements.push(element);
      } // end if
    } // end for
    return elements;
  },
  render: function() {
    return (
      React.createElement('div', {},
        this.renderItems()
      )
    );
  }
});
/////////////////////////////////////////
// x. BODY HIGHLIGHTER COMPONENT
var BodyHighlighterComponent = React.createClass({
  propTypes: {
     highlighters: React.PropTypes.array
  },
  render: function() {
    return (
      React.createElement('div', {},
        this.props.highlighters.map(function(h, i) {
          var connectorText = 'connector-organ-'+h[i].position;
            var contentText = 'connector-text-organ-'+h[i].position;
          return (
              React.createElement('div', {key: i},
                React.createElement('div', {className: connectorText}),
                  React.createElement('div', {className: contentText, title: h[i].text}, h[i].text)
            )
          );
        })
      )
    );
  }
});
/////////////////////////////////////////
// x. SEQUENCE BROWSER COMPONENT
var SequenceBrowserComponent = React.createClass({

  propTypes: {
      gene: React.PropTypes.any,
      exon: React.PropTypes.any,
      snp: React.PropTypes.any,
      exonLevel: React.PropTypes.func,
      sequenceLevel: React.PropTypes.func,
      justifyPosition: React.PropTypes.func,
      handleResizeOnVariation: React.PropTypes.func
  },
  componentDidMount: function() {
      var data = this.handlePosition(this.props.exon, this.props.snp);
      //this.props.justifyPosition(data[2]);
      window.addEventListener('resize', this.handleResizeOnVariation);

  },
  handleResizeOnVariation: function () {
      var data = this.handlePosition(this.props.exon, this.props.snp);
      this.props.handleResizeOnVariation(data[2]);
  },
  handleMoveNext: function() {
      var leftPos = jQuery('.variation-bar').scrollLeft()+450;
      jQuery(".variation-bar").stop().animate({scrollLeft: leftPos }, 400);
      if (jQuery('.variation-bar').attr('leftPos') != leftPos) {
        jQuery('.variation-bar').attr('leftPos',leftPos);
      } else {
        this.props.handleAjaxLoadSequence(1000);
      }
  },
  handleMoveBack: function() {
      var leftPos = jQuery('.variation-bar').scrollLeft();
      if (leftPos > 0) {
          jQuery(".variation-bar").stop().animate({scrollLeft: leftPos - 450}, 400);
      }else {
          this.props.handleAjaxLoadSequence(-1000);
      }
  },
  handleExonLevel: function(k) {
    this.props.exonLevel(k);
  },
  handleSequenceLevel: function(k) {
    this.props.sequenceLevel(k);
  },
  handleCheckShowSNPName: function() {
    var eles = document.getElementsByClassName('snpName');
    for (var i = 0; i < eles.length; ++i) {
      eles[i].style.display = (eles[i].style.display == 'none') ? 'inline-block' : 'none';
    }
  },
  handleToggleSNPName: function(k) {
    // var name = 'snp-'+k;
    // var ele = document.getElementById(name);
    // ele.style.display = (ele.style.display == 'none') ? 'inline-block' : 'none';
  },
  handleToggleIndicator: function (name){
      var elements = document.getElementsByClassName(name);
      for (var i = 0; i < elements.length; i++) {
           elements[i].style.display = (elements[i].style.display == 'block') ? 'none' : 'block';
      }
  },
  handlePosition: function(exon, snp) {
    var terminal = Math.floor(exon.end - exon.start);
    var exonStart = 0;
    var exonEnd = terminal;
    var snpPosition = (snp.position - exon.start);

  return [exonStart, exonEnd, snpPosition];
  },
	//////////////////////////////////////////////////////////////////////////////
	// RENDER
  renderSNPNameCheckbox: function() {
    return (
      React.createElement('div', {className: 'leftGroup'},
        React.createElement('input', {className: 'snpNameCheckBox', type: 'checkbox', onClick: this.handleCheckShowSNPName, defaultChecked: true }),
        React.createElement('span', {}, "Show variations names")
      )
    );
  },
  renderControlPanel: function () {
    return (
      React.createElement('div', {className: 'sequenceControlBtnGroup'},
        this.renderSNPNameCheckbox(),
        React.createElement('div', {className: 'rightGroup'},
          React.createElement('div', {className: 'viewlevel'}, 'Magnification level: Sequence'),
          React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-left', onClick: this.handleMoveBack }),
					React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-right', onClick: this.handleMoveNext })
        )
      )
    );
  },
  renderSequencePointer: function generatePointer(exon, snp, position) {
    var mappingLetter = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'};
    var elements = [];
    var str = this.props.exon.sequence;
    var stringTop = str!=null ? str.split(""):[];
    var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];
    var index = 0;

    var data = this.handlePosition(exon, snp);
    var exonStart = data[0];
    var exonEnd = data[1];
    var snpPosition = data[2];


    for(i = data[0]; i < data[1]; i++){
      var element;
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
      attr.onMouseOver = root.handleToggleIndicator.bind(null, 'indicator-'+i);
      attr.onMouseOut = root.handleToggleIndicator.bind(null, 'indicator-'+i);
      attr.onMouseEnter = root.handleToggleSNPName.bind(null, i);

      var attrIndicator = {};
      attrIndicator.style = {};
      attrIndicator.className = 'indicator ' + 'indicator-'+i;


      element = React.createElement('div', attr);
      // Exon
      if (i >= exonStart && i <= exonEnd) {
        attr.className = attr.className +' pointer-hightlight';
        element = React.createElement('div', attr);

        if (snpPosition == i) {
          var color = ' snp-mutation-hightlight';
          attr.className = attr.className + color + ' variation-pointer';
          attrLetterAbove.id = (position === 'top') ? 'letter-variation-top-top' : 'letter-variation-bottom-top';
          attrLetterAbove.className = attrLetterAbove.className + ' letter-mutation';
          attrIndicator.style.display = 'inline';
          attrLetterBottom.id = (position === 'top') ? 'letter-variation-top-bottom' : 'letter-variation-bottom-bottom';
          attrSequence.id = (position === 'top') ? 'sequence-ex-top' : 'sequence-ex-bottom';
          element = React.createElement('div', attr);
        }
      }
      elements.push(
        React.createElement('div', attrSequence,
          React.createElement('div', attrBehind,
            React.createElement('div', attrLetterAbove, letterTop),
            element,
            React.createElement('div', attrLetterBottom, letterBottom)
          ),
          React.createElement('div', attrIndicator)
        )
      );
      index++;
    }
    return elements;
  },
  renderSequenceName: function generateGeneName(snp) {

    var key = Math.floor((Math.random() * 10) + 1);
    var elements = [];
    var root = this;
    var range = 0;

    var snpPosition = (snp.position - snp.exon.start);
    var position = ((snpPosition - range) * 9).toString()+'px';

    var attrParent = {};
    attrParent.style = {};
    attrParent.key = key;
    attrParent.className = 'topName';
    //attrParent.style.marginLeft = position;
    elements.push(React.createElement('div', attrParent,
      React.createElement('span', {className: 'light'}, snp.geneId + " gene")
      // React.createElement('span', {}, ' '+snp.exon.exonId)
    ));

    var attr = {};
    attr.className = 'snpName';
    attr.id = 'snpName';
    attr.key = key + 1;
    attr.style = {};
    attr.style.marginLeft = position;
    console.log(snp.reversed);
    var tokens = (snp.reversed) ? snp.allele.split("/").reverse() : snp.allele.split("/");
    var text = snp.rsnumber + " [" + tokens.join(">") + "] ";
    elements.push(
      React.createElement('p', attr, text)
    );
    return elements;
  },
  renderSequenceLevel: function(exon, snp) {
    return (
      React.createElement('div', {className: 'inner_con_banner'},
        React.createElement('div', {id: 'sequence-panel'},
          // Variation bar
          React.createElement('div', {className: 'variation-bar-top variation-bar'},
            // Name bar top
            React.createElement('div', {className: 'variation-name-bar'},
              this.renderSequenceName(snp)
            ),
            // Pointer bar top
            React.createElement('div', {className: 'variation-pointer-top'},
                this.renderSequencePointer(exon, snp, 'top')
              )
          ),
          React.createElement('div', {className: 'variation-bar-bottom variation-bar'},
             // Name bar bottom
            React.createElement('div', {className: 'variation-name-bar'},
              this.renderSequenceName(snp)
            ),
             // Pointer bar bottom
            React.createElement('div', {className: 'variation-pointer-bottom'},
                this.renderSequencePointer(exon, snp, 'bottom')
            )
          ),
          // Control pannel
          this.renderControlPanel()
        )
      )
    );
  },
  render: function() {
      return this.renderSequenceLevel(this.props.exon, this.props.snp);
  }
});
