var BannerComponent = React.createClass({
  getInitialState : function() {
      // console.log(this.props.data);
      var viewerRangeArr = [[0, 371], [0, 295], [0, 116]];
      var viewerLengthArr = [100, 60, 20];
      return {
        showSNPName: true,
        indexLetter: 0,
        // chromosome: {
        //      	chromosomeNumber: this.props.data.chromosomeId,
        //      	numGene: this.props.data.numOfGenes,
        //      	numSNP: this.props.data.numOfSNPs,
         //    numDisease: this.props.data.numOfDiseases,
         //    numTrait: this.props.data.numOfTraits
        //  	},
        chromosome: this.props.data.chromosome,
        chromosomeHighlighter: [this.props.data.chromosomeHighlight],
        // bodyHighlighter: [
       //    	this.props.data.bodyHighlighter
        // ],
        geneSequence: {
            drillLevel: this.props.drillLevel,
            viewerLength: viewerLengthArr[this.props.drillLevel],
            viewerRange: viewerRangeArr[this.props.drillLevel],
            chromosome: this.props.data,
            gene: this.props.data,
            exon: this.props.data.exon,
            snp: this.props.data
        }
      };
    },
      componentDidMount: function() {
          var root = this;
          jQuery('.potential').click(function() {
              var mappingLetter = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'};
              var potentialPair = jQuery(this).text().split('/');
              var topLetterTop = potentialPair[0];
              var topLetterBottom = mappingLetter[topLetterTop];
              var bottomLetterTop = potentialPair[1];
              var bottomLetterBottom = mappingLetter[bottomLetterTop];

              // Scroll up
              jQuery("html, body").animate({ scrollTop: 280 }, 800);

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
      },
    moveSequenceNext: function() {
      var geneSequence = this.state.geneSequence;
      geneSequence.viewerRange[0] = geneSequence.viewerRange[0] + this.state.geneSequence.viewerLength;
      geneSequence.viewerRange[1] = geneSequence.viewerRange[1] + this.state.geneSequence.viewerLength;
      var indexLetter = this.state.indexLetter;
      indexLetter = indexLetter + this.state.geneSequence.viewerLength;
      this.setState({
        geneSequence: geneSequence,
        indexLetter: indexLetter
      });
    },
    moveSequenceBack: function() {
          var geneSequence = this.state.geneSequence;
      var geneSequence = this.state.geneSequence;
      var indexLetter = this.state.indexLetter;
          var length = this.state.geneSequence.viewerLength;
      if (geneSequence.viewerRange[0] > 0) {
              if (geneSequence.viewerRange[0] < length) {
                  length = geneSequence.viewerRange[0];
              }
        geneSequence.viewerRange[0] = geneSequence.viewerRange[0] - length;
        geneSequence.viewerRange[1] = geneSequence.viewerRange[1] - length;

        indexLetter = indexLetter - length;
      }
      this.setState({
        geneSequence: geneSequence,
        indexLetter: indexLetter
      });
    },
      handleResizeOnChromosome: function() {
          var parentWidth = Math.floor(jQuery('.inner_con_banner').width());
          var proportion = Math.floor(parentWidth/4); // 5 is 5px, the width of a pointer
          var geneSequence = this.state.geneSequence;
          geneSequence.viewerRange[0] = 0;
          geneSequence.viewerRange[1] = (proportion - 1);

          this.setState({
              geneSequence: geneSequence
          });

      },
      handleResizeOnGene: function() {
          var parentWidth = Math.floor(jQuery('.inner_con_banner').width());
          var proportion = Math.floor(parentWidth/5); // 5 is 5px, the width of a pointer
          var geneSequence = this.state.geneSequence;
          geneSequence.viewerRange[0] = 0;
          geneSequence.viewerRange[1] = (proportion - 1);

          this.setState({
              geneSequence: geneSequence
          });

      },
      handleResizeOnVariation: function(data) {
          var parentWidth = Math.floor(jQuery('.inner_con_banner').width());
          var proportion = Math.floor(parentWidth/9); // 9 is 9px, the width of a pointer
          var snpPosition = (data/proportion);
          var geneSequence = this.state.geneSequence;
          geneSequence.viewerRange[0] = (Math.floor(snpPosition) * proportion);
          geneSequence.viewerRange[1] = (Math.ceil(snpPosition) * proportion);
          // var indexLetter = this.state.indexLetter;
          var indexLetter = (Math.floor(snpPosition) * proportion);

          this.setState({
              geneSequence: geneSequence,
              indexLetter: indexLetter
          });
      },
    justifyPosition: function(data) {
          var parentWidth = Math.floor(jQuery('.inner_con_banner').width());
          if (parentWidth % 2 != 0) {
              parentWidth = parentWidth - 3;
          }
          var proportion = Math.floor(parentWidth/9); // 9 is 9px, the width of a SNP

      var snpPosition = (data/proportion);
          var geneSequence = this.state.geneSequence;
          geneSequence.viewerRange[0] = (Math.floor(snpPosition) * proportion);
          geneSequence.viewerRange[1] = (Math.ceil(snpPosition) * proportion);
          var indexLetter = this.state.indexLetter;
          indexLetter = indexLetter + (Math.floor(snpPosition) * proportion);

          this.setState({
              geneSequence: geneSequence,
              indexLetter: indexLetter
          });
    },
    geneLevel: function() {
      // View Chromosome level
    },
    exonLevel: function(k) {
      var href = '/gene/'+this.state.geneSequence.gene.geneId;
      window.location.href = href;
    },
    sequenceLevel: function(k) {
      if (this.state.geneSequence.exon[k].hasOwnProperty('snps')) {
        if (this.state.geneSequence.exon[k].snps.length > 0) {
          var href = '/variation/'+this.state.geneSequence.exon[k].snps[0];
          window.location.href = href;
        }
      }
    },
    checkShowSNPName: function() {
      this.setState({showSNPName: !this.state.showSNPName});
    },
    hoverShowSNPName: function(k) {
      if (this.state.showSNPName == false) {
        var name = 'snp-'+k;
        var eles = document.getElementsByClassName(name);
        for (var i = 0; i < eles.length; ++i) {
          var ele = eles[i];
          ele.style.display = 'inline';
      }
    }
    },
    hoverHideSNPName: function(k) {
      if (this.state.showSNPName == false) {
        var name = 'snp-'+k;
        var eles = document.getElementsByClassName(name);
        for (var i = 0; i < eles.length; ++i) {
          var ele = eles[i];
          ele.style.display = 'none';
      }
      }
    },
    zoomIn: function() {
      var geneSequence = this.state.geneSequence;
      if (geneSequence.drillLevel == 0) {
        this.exonLevel(0);
      } else if (geneSequence.drillLevel == 1) {
        var root = this;
        this.state.geneSequence.exon.map(function(i, k) {
          root.sequenceLevel(k)
        });
      }
      this.setState({geneSequence: geneSequence});
    },
    zoomOut: function() {
      var geneSequence = this.state.geneSequence;
      if (geneSequence.drillLevel == 2) {
        this.exonLevel(0);
      } else if (geneSequence.drillLevel == 1) {
        this.geneLevel();
      }
      this.setState({geneSequence: geneSequence});
    },
  render: function() {
    var chromosomeHighlightComponent = (this.state.geneSequence.drillLevel == 2) ? React.createElement(chromosomeHighlighterComponent, { highlighters: this.state.chromosomeHighlighter }) : '';
    // var bodyHighlightComponent = (this.state.geneSequence.drillLevel == 2) ? React.createElement(BodyHighlighterComponent, {
    // 			highlighters: this.state.bodyHighlighterasd
    // 		}) : '';
    return (
      React.createElement('div', {className: 'images_secs'},
        React.createElement(ChromosomeComponent, {chromosome: this.state.chromosome}),
        chromosomeHighlightComponent,
        React.createElement('img', {className: 'img-chrom-body ', src: this.props.imgSrc}),
        React.createElement(SequenceBrowserComponent, {
          drillLevel: this.state.geneSequence.drillLevel,
          indexLetter: this.state.indexLetter,
                viewerLength: this.state.geneSequence.viewerLength,
                viewerRange: this.state.geneSequence.viewerRange,
                chromosome: this.state.geneSequence.chromosome,
                gene: this.state.geneSequence.gene,
                exon: this.state.geneSequence.exon,
                snp: this.state.geneSequence.snp,
                related: this.state.geneSequence.related,
                showSNPName: this.state.showSNPName,
                sequence: this.state.geneSequence.sequence,
                // Funcs
                moveNext: this.moveSequenceNext,
                moveBack: this.moveSequenceBack,
                exonLevel: this.exonLevel,
                sequenceLevel: this.sequenceLevel,
                checkShowSNPName: this.checkShowSNPName,
                hoverShowSNPName: this.hoverShowSNPName,
                hoverHideSNPName: this.hoverHideSNPName,
                justifyPosition: this.justifyPosition,
                      handleResizeOnVariation: this.handleResizeOnVariation,
                      handleResizeOnGene: this.handleResizeOnGene,
                      handleResizeOnChromosome: this.handleResizeOnChromosome,
                zoomIn: this.zoomIn,
                zoomOut: this.zoomOut
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
              React.createElement('p', {}, this.props.chromosome.numOfSNPs + ' snps'),
              React.createElement('p', {}, this.props.chromosome.numOfDiseases + ' diseases'),
              React.createElement('p', {}, this.props.chromosome.numOfTraits + ' trais')
          )
        )
      )
    );
  }
});
/////////////////////////////////////////
// x. CHROMOSOME HIGHLIGHTER COMPONENT
var chromosomeHighlighterComponent = React.createClass({
  propTypes: {
  highlighters: React.PropTypes.array
  },
  render: function() {
    return (
      React.createElement('div', {},
        this.props.highlighters.map(function(h, i) {
          var text = h.text.split(",");
            var areaText = 'chrom'+h.index.toString();
            var connectorText = 'connector-chrom'+h.index.toString();
            var contentText = 'connector-text-chrom'+h.index.toString();

            return (
              React.createElement('div', {key: i},
                React.createElement('div', {className: areaText, title: "Chromosome "+h.chromosome}),
                React.createElement('div', {className: connectorText, title: "Chromosome "+h.chromosome}),
                React.createElement('div', {className: contentText},
                  text.map(function(t, i) {
                    return (React.createElement('p', {key: i}, t));
                  })
                )
              )
          )
        })
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
      drillLevel: React.PropTypes.number,
      indexLetter: React.PropTypes.number,
      viewerLength: React.PropTypes.number,
      viewerRange: React.PropTypes.array,
      gene: React.PropTypes.any,
      exon: React.PropTypes.any,
      snp: React.PropTypes.any,
      sequence: React.PropTypes.string,
      showSNPName: React.PropTypes.bool,
      sequence: React.PropTypes.string,
      moveNext: React.PropTypes.func,
      moveBack: React.PropTypes.func,
      exonLevel: React.PropTypes.func,
      sequenceLevel: React.PropTypes.func,
      checkShowSNPName: React.PropTypes.func,
      hoverShowSNPName: React.PropTypes.func,
      hoverHideSNPName: React.PropTypes.func,
      justifyPosition: React.PropTypes.func,
      handleResizeOnVariation: React.PropTypes.func,
      handleResizeOnGene: React.PropTypes.func,
      zoomIn: React.PropTypes.func,
      zoomOut: React.PropTypes.func,
  },
  componentDidMount: function() {
    if (this.props.drillLevel == 2) { // SNP
      var data = this.handlePosition(this.props.exon, this.props.snp);
          this.props.justifyPosition(data[2]);
          window.addEventListener('resize', this.handleResizeOnVariation);
    } else if (this.props.drillLevel == 1) { // Gene
          this.handleResizeOnGene();
          window.addEventListener('resize', this.handleResizeOnGene);
      } else if (this.props.drillLevel == 0) { // Chromosome
          this.handleResizeOnChromosome();
          window.addEventListener('resize', this.handleResizeOnChromosome);
      }
  },
  handleResizeOnChromosome: function () {
      this.props.handleResizeOnChromosome();
  },
  handleResizeOnGene: function () {
      this.props.handleResizeOnGene();
  },
  handleResizeOnVariation: function () {
      var data = this.handlePosition(this.props.exon, this.props.snp);
      this.props.handleResizeOnVariation(data[2]);
  },
  handleMoveNext: function() {
    this.props.moveNext();
  },
  handleMoveBack: function() {
    this.props.moveBack();
  },
  handleExonLevel: function(k) {
    this.props.exonLevel(k);
  },
  handleSequenceLevel: function(k) {
    this.props.sequenceLevel(k);
  },
  handleCheckShowSNPName: function() {
    this.props.checkShowSNPName();
  },
  handleHoverShowSNPName: function(k) {
    this.props.hoverShowSNPName(k);
  },
  handleHoverHideSNPName: function(k) {
    this.props.hoverHideSNPName(k);
  },
  handleHoverShowExonName: function(k) {
    var exonName = 'exon-'+k;
    var element = document.getElementById(exonName);
    element.style.display =  'inline';
  },
  handleHoverHideExonName: function(k) {
    var exonName = 'exon-'+k;
    var element = document.getElementById(exonName);
    element.style.display =  'none';
  },
  handleZoomIn: function() {
    this.props.zoomIn();
  },
  handleZoomOut: function() {
    this.props.zoomOut();
  },
  showIndicator: function (name){
      var elements = document.getElementsByClassName(name)
      for (var i = 0; i < elements.length; i++) {
           elements[i].style.display = 'block';
      }
  },
  hideIndicator: function (name){
      var elements = document.getElementsByClassName(name)
      for (var i = 0; elements[i]; i++) {
           elements[i].style.display = 'none';
      }
  },
  // handleJustifyPosition: function (start, end, exon, snp) {
  //     var data = this.handlePosition(exon, snp);
  //     var snpPosition = data[2];
  //     var extra = (start + end)/2;
  //     var nStart = (snpPosition - extra);
  //     var nEnd = (snpPosition + extra);

  //     return [nStart, nEnd];
  // },
  handlePosition: function(exon, snp) {
    var terminal = Math.floor(exon.end - exon.start);
  var exonStart = 0;
  var exonEnd = terminal;
  var snpPosition = (snp.position - exon.start);

  return [exonStart, exonEnd, snpPosition];
  },
	handleExonSequenceMoveNext: function() {
	  var leftPos = jQuery('.exon-bar').scrollLeft();
	  jQuery(".exon-bar").animate({scrollLeft: leftPos + 250}, 500);
	},
	handleExonSequenceMoveBack: function() {
	  var leftPos = jQuery('.exon-bar').scrollLeft();
		if (leftPos > 0) {
				jQuery(".exon-bar").animate({scrollLeft: leftPos - 250}, 500);
		}
	},
	//////////////////////////////////////////////////////////////////////////////
	// RENDER
  renderSNPNameCheckbox: function() {
    return (
      React.createElement('div', {className: 'leftGroup'},
        React.createElement('input', {className: 'snpNameCheckBox', type: 'checkbox', onClick: this.handleCheckShowSNPName, defaultChecked: this.props.showSNPName }),
        React.createElement('span', {}, "Show SNP names")
      )
    );
  },
  renderControlPanel: function () {
    var checkbox = (this.props.drillLevel == 2) ? this.renderSNPNameCheckbox() : '';
    var drillLevelText = ['Gene', 'Exon', 'Sequence'];
    return (
      React.createElement('div', {className: 'sequenceControlBtnGroup'},
        checkbox,
        React.createElement('div', {className: 'rightGroup'},
          React.createElement('div', {className: 'viewlevel'}, 'Magnification level: '+(drillLevelText[this.props.drillLevel])),
					this.renderBackButton(),
          React.createElement('span', {className: 'fa fa-search-plus sequenceZoomControlBtn', onClick: this.handleZoomIn }),
          React.createElement('span', {className: 'fa fa-search-minus sequenceZoomControlBtn', onClick: this.handleZoomOut }),
					this.renderNextButton()
        )
      )
    );
  },

	renderNextButton: function () {
		var nextBtn = '';
		var drillLevel = this.props.drillLevel;
		if (drillLevel == 0) {
			var nextBtn =	React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-right', onClick: this.handleMoveNext });
		}	else if (drillLevel == 1) {
			var nextBtn = React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-right', onClick: this.handleExonSequenceMoveNext });
		} else if (drillLevel == 2) {
		var nextBtn =	React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-right', onClick: this.handleMoveNext });
		}
		return nextBtn;
	},
	renderBackButton: function () {
		var backBtn = '';
		var drillLevel = this.props.drillLevel;
		if (drillLevel == 0) {
			var backBtn =	React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-left', onClick: this.handleMoveBack });
		}	else if (drillLevel == 1) {
			var backBtn = React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-left', onClick: this.handleExonSequenceMoveBack });
		} else if (drillLevel == 2) {
		var backBtn =	React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-left', onClick: this.handleMoveBack });
		}
		return backBtn;
	},
  renderGenePointer: function generatePointer(first, last, genes) {
  var elements = [];
  var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];
      var highlighter = ['pointer-hightlight-light', 'pointer-hightlight-dark'];

      genes.sort(function(a, b) {
          if (a.start < b.start)
              return -1;
          if (a.start > b.start)
              return 1;
          return 0;
      });

      var start = genes[0].start;
      var end = genes[genes.length-1].end;
      var terminal = Math.floor((end - start) / 150);

  for(i = first; i < last; i++){
    var root = this;
    var attr = {};
    attr.key = i;
    attr.className = 'gene-pointer pointer';
    attr.className = attr.className + ' icon-Gen'+mapping[i%6];

    genes.map(function(gene, k) {
      var startC = (Math.floor((gene.start - start) / 150));
      var endC = terminal - Math.floor((end - gene.end) / 150);
      if (i >= startC && i <= endC) {
          attr.className = attr.className +' '+highlighter[k%2];
          attr.onClick = root.handleExonLevel.bind(null, k);
          attr.key = k;
      }
    });
    elements.push(React.createElement('div', attr));
  }

  return elements;
},
renderExonPointer: function generatePointer(first, last, exon, geneStart, geneEnd) {
  var elements = [];
  var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];
  exon.sort(function(a,b) {
    if (a.start < b.start)
      return -1;
      if (a.start > b.start)
        return 1;
      return 0;
  });

  ////////////////////////////////////////////////////////////////////////////
  var start = exon[0].start;
  var end = exon[exon.length-1].end;
  var terminal = Math.floor((end - start) / 20);
  var geneTerminal = Math.floor((geneEnd - geneStart) / 20);
  var exonMap = [];
  exon.map(function(e, k) {
    var startC = (Math.floor((e.start - start) / 20));
    var endC = terminal - Math.floor((end - e.end) / 20);
    var numSnps = (e.hasOwnProperty('snps')) ? e.snps.length : 0;
    var exonMapItem = {point: parseInt(endC - startC), numSnps: numSnps}
    exonMap.push(exonMapItem);
  });
  ////////////////////////////////////////////////////////////////////////////

  var pointerIndicate = 0;
	var randomPointer = 5;
	// Some while pointers at the head
	for (var k = 0; k < randomPointer; k++) {
		var attrGeneWrapper = {};
		attrGeneWrapper.className = 'gene-wrapper';
    attrGeneWrapper.key = k;
		var attr = {};
		attr.className = 'exon-pointer pointer';
		attr.className = attr.className + ' icon-Gen'+mapping[pointerIndicate%6];
		elements.push(
			React.createElement('div', {className: 'exon-sequence'},
					React.createElement('div', attrGeneWrapper,
							React.createElement('div', attr)
					)
			)
		);
		pointerIndicate = pointerIndicate + 1;
	}
	///////////////////////////////////
  for (var i = 0; i < exonMap.length; i++) {
    var point = exonMap[i].point;
    var numSnps = exonMap[i].numSnps;
    for (var j = 1; j <= point; j++) {
      var root = this;
      var attrGeneWrapper = {};
      attrGeneWrapper.className = 'gene-wrapper gene-wrapper-color';
      var attr = {};
      var color = (numSnps > 0) ? ' light' : ' gray';
      attr.className = 'exon-pointer pointer';
      attr.className = attr.className + ' icon-Gen'+mapping[pointerIndicate%6];
      attr.className = attr.className + color;
      attr.onClick = root.handleSequenceLevel.bind(null, i);
      // attr.onMouseOver = root.handleHoverShowExonName.bind(null, k);
      // attr.onMouseLeave = root.handleHoverHideExonName.bind(null, k);
      attr.title = ((numSnps > 0) ? numSnps.toString() : "0") + " snps in this exon"; // Temperation
      elements.push(
        React.createElement('div', {className: 'exon-sequence'},
            React.createElement('div', attrGeneWrapper,
                React.createElement('div', attr)
            )
        )
      );
      pointerIndicate = pointerIndicate + 1;
    }

    for (var k = 0; k < randomPointer; k++) {
      var attrGeneWrapper = {};
      attrGeneWrapper.className = 'gene-wrapper gene-wrapper-color';
      attrGeneWrapper.key = k;
      var attr = {};
      attr.className = 'exon-pointer pointer';
      attr.className = attr.className + ' icon-Gen'+mapping[pointerIndicate%6];
      elements.push(
        React.createElement('div', {className: 'exon-sequence'},
            React.createElement('div', attrGeneWrapper,
                React.createElement('div', attr)
            )
        )
      );
      pointerIndicate = pointerIndicate + 1;
    }
  }
	// Some while pointers at the tail
	for (var k = 0; k < randomPointer; k++) {
		var attrGeneWrapper = {};
		attrGeneWrapper.className = 'gene-wrapper';
		var attr = {};
		attr.className = 'exon-pointer pointer';
		attr.className = attr.className + ' icon-Gen'+mapping[pointerIndicate%6];
		elements.push(
			React.createElement('div', {className: 'exon-sequence'},
					React.createElement('div', attrGeneWrapper,
							React.createElement('div', attr)
					)
			)
		);
		pointerIndicate = pointerIndicate + 1;
	}
	///////////////////////////////////
  return elements;
},
renderSequenceTopPointer: function generatePointer(start, end, exon, snp) {
  var mappingLetter = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'};
  var elements = [];
  var str = this.props.exon.sequence;
  var stringTop = str.split("");
  var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];
  var index = this.props.indexLetter;

  var data = this.handlePosition(exon, snp);
  var exonStart = data[0];
  var exonEnd = data[1];
  var snpPosition = data[2];

  for(i = start; i < end; i++){
    var element;
    var letterTop = stringTop[index];
    var letterBottom = mappingLetter[letterTop];
    var root = this;

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
    attr.onMouseOver = root.showIndicator.bind(null, 'indicator-'+i);
    if (i != snpPosition) {
        attr.onMouseOut = root.hideIndicator.bind(null, 'indicator-'+i);
    }

    var attrIndicator = {};
    attrIndicator.style = {};
    attrIndicator.className = 'indicator ' + 'indicator-'+i;

    if (!root.props.showSNPName) {
      attr.onMouseEnter = root.handleHoverShowSNPName.bind(null, i);
    }
    if (!root.props.hideSNPName) {
      attr.onMouseLeave = root.handleHoverHideSNPName.bind(null, i);
    }
    element = React.createElement('div', attr);
    // Exon
    if (i >= exonStart && i <= exonEnd) {
      var root = this;
      attr.className = attr.className +' pointer-hightlight';
      element = React.createElement('div', attr);

      if (snpPosition == i) {
        var color = ' snp-mutation-hightlight';
        attr.className = attr.className + color + ' variation-pointer';
                  attrLetterAbove.id = 'letter-variation-top-top';
                  attrLetterAbove.className = attrLetterAbove.className + ' letter-mutation';
                  attrIndicator.style.display = 'inline';
                  attrLetterBottom.id = 'letter-variation-top-bottom';
                  attrSequence.id = 'sequence-ex-top';
        element = React.createElement('div', attr);
      }
    }
    elements.push(
      React.createElement('div', attrSequence,
                  React.createElement('div', {className: 'behind'},
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
  renderSequenceBottomPointer: function generatePointer(start, end, exon, snp) {
      var mappingLetter = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'};
      var elements = [];
      var str = this.props.exon.sequence;
      var stringTop = str.split("");
      var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];
      var index = this.props.indexLetter;

      var data = this.handlePosition(exon, snp);
      var exonStart = data[0];
      var exonEnd = data[1];
      var snpPosition = data[2];

      for(i = start; i < end; i++){
          var element;
          var letterTop = stringTop[index];
          var letterBottom = mappingLetter[letterTop];
          var root = this;

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
          attr.onMouseOver = root.showIndicator.bind(null, 'indicator-'+i);
          if (i != snpPosition) {
              attr.onMouseOut = root.hideIndicator.bind(null, 'indicator-'+i);
          }

          var attrIndicator = {};
          attrIndicator.style = {};
          attrIndicator.className = 'indicator ' + 'indicator-'+i;

          if (!root.props.showSNPName) {
              attr.onMouseEnter = root.handleHoverShowSNPName.bind(null, i);
          }
          if (!root.props.hideSNPName) {
              attr.onMouseLeave = root.handleHoverHideSNPName.bind(null, i);
          }
          element = React.createElement('div', attr);
          // Exon
          if (i >= exonStart && i <= exonEnd) {
              var root = this;
              attr.className = attr.className +' pointer-hightlight';
              element = React.createElement('div', attr);

              if (snpPosition == i) {
                  var color = ' snp-mutation-hightlight';
                  attr.className = attr.className + color + ' variation-pointer';
                  attrLetterAbove.id = 'letter-variation-bottom-top';
                  attrLetterAbove.className = attrLetterAbove.className + ' letter-mutation';
                  attrIndicator.style.display = 'inline';
                  attrLetterBottom.id = 'letter-variation-bottom-bottom';
                  attrSequence.id = 'sequence-ex-bottom';
                  element = React.createElement('div', attr);
              }
          }
          elements.push(
              React.createElement('div', attrSequence,
                  React.createElement('div', {className: 'behind'},
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
renderGeneName: function generateGeneName(range, genes) {
  var elements = [];
      var highlighter = ['pointer-hightlight-light', 'pointer-hightlight-dark'];

      genes.sort(function(a,b) {
          if (a.start < b.start)
              return -1;
          if (a.end > b.end)
              return 1;
          return 0;
      });

      var start = genes[0].start;
  genes.map(function(gene, i) {
    var startC = (Math.floor((gene.start - start) / 150));
    var position = ((startC - range) * 4).toString()+'px';
    var name = gene.name;
    var attr = {};
    attr.style = {};

    attr.style.marginLeft = position;
    attr.className = 'geneName';
    attr.key = i;
    elements.push(React.createElement('div', attr,
      React.createElement('div', {key: i, className: highlighter[i%2]}, name)
    ));
  });
  return elements;
},
renderExonName: function generateGeneName(gene, exon) {
  var elements = [];
  var root = this;

  exon.sort(function(a,b) {
      if (a.start < b.start)
          return -1;
      if (a.end > b.end)
          return 1;
      return 0;
  });

	////////////////////////////////////////////////////////////////////////////
  var start = exon[0].start;
  var end = exon[exon.length-1].end;
  var terminal = Math.floor((end - start) / 20);
  var exonMap = [];
  exon.map(function(e, k) {
  var startC = (Math.floor((e.start - start) / 20));
  var endC = terminal - Math.floor((end - e.end) / 20);
  var numSnps = (e.hasOwnProperty('snps')) ? e.snps.length : 0;
  var exonMapItem = {point: parseInt(endC - startC), numSnps: numSnps}
  exonMap.push(exonMapItem);
  });
  ////////////////////////////////////////////////////////////////////////////
	var tracker = 5;
	for (var i = 0; i < exonMap.length; i++) {
		var e = exonMap[i];
    console.log(e);
		var position = ((tracker) * 5).toString()+'px';
    console.log(position);
		tracker = tracker + (e.point + 5);

		var attr = {};
    var color = ' light';

		attr.style = {};
		attr.style.marginLeft = position;
		attr.style.display = 'inline';
		attr.className = 'exonName';
    attr.className = attr.className + color;
		attr.id = 'exon-'+i;
		attr.key = i;
		var exonName = "Exon" + " " + (i + 1).toString();
		elements.push(
			React.createElement('div', attr, exonName)
		);
	}

  return (
      React.createElement('div',{},
        React.createElement('div', {},
					React.createElement('span', {className: 'topName'}, gene.name)
				),
        elements
      )
  );
},
renderSequenceName: function generateGeneName(range, snp) {
  var elements = [];
  var root = this;

  var attrParent = {};
  attrParent.style = {};
  attrParent.className = 'snpName'
  attrParent.style.marginLeft = position;
  // console.log(snp);
  elements.push(React.createElement('div', attrParent,
    React.createElement('span', {className: 'light'}, snp.geneId),
    React.createElement('span', {}, ' '+snp.exon.exonId)
  ));
  var snpPosition = (snp.position - snp.exon.start);
  var position = ((snpPosition - range)*9).toString()+'px';
  var attr = {};
  attr.key = 1;
      attr.className = 'snpName'
  attr.style = {};
  attr.style.display = (this.props.showSNPName) ? 'inline' : 'none';
  attr.style.marginLeft = position;
  attr.text = snp.rsnumber + " [" + snp.allele.split("/").join(">") + "] ";
  elements.push(
    React.createElement('p', attr, attr.text)
  );
  return elements;
},
  renderGeneLevel: function() {
    return (
      React.createElement('div', {className: 'inner_con_banner'},
        React.createElement('div', {},
          React.createElement('div', {className: 'gene-bar-top'},
            React.createElement('div', {className: 'sequenceGenesName'},
              this.renderGeneName(this.props.viewerRange[0], this.props.chromosome.genes)
            ),
            React.createElement('div', {className: 'genStringTop genCommon'},
                this.renderGenePointer(this.props.viewerRange[0],this.props.viewerRange[1], this.props.chromosome.genes)
              )
          ),
          React.createElement('div', {className: 'gene-bar-bottom'},
            React.createElement('div', {className: 'sequenceGenesName'},
              this.renderGeneName(this.props.viewerRange[0], this.props.chromosome.genes)
            ),
            React.createElement('div', {className: 'genStringBottom genCommon'},
                this.renderGenePointer(this.props.viewerRange[0],this.props.viewerRange[1], this.props.chromosome.genes)
            )
          ),
          this.renderControlPanel()
        )
      )
    );
  },
  renderExonLevel: function() {
    return (
      React.createElement('div', {className: 'inner_con_banner'},
        React.createElement('div', {},
          React.createElement('div', {className: 'exon-bar-top exon-bar'},
            React.createElement('div', {className: 'sequenceGenesName'},
              this.renderExonName(this.props.gene, this.props.exon)
            ),
            React.createElement('div', {className: 'exon-pointer-top'},
                this.renderExonPointer(this.props.viewerRange[0], this.props.viewerRange[1], this.props.exon, this.props.gene.start, this.props.gene.end)
              )
          ),
          React.createElement('div', {className: 'exon-bar-bottom exon-bar'},
            React.createElement('div', {className: 'sequenceGenesName'},
              this.renderExonName(this.props.gene, this.props.exon)
            ),
            React.createElement('div', {className: 'exon-pointer-bottom'},
                this.renderExonPointer(this.props.viewerRange[0], this.props.viewerRange[1], this.props.exon, this.props.gene.start, this.props.gene.end)
            )
          ),
          this.renderControlPanel()
        )
      )
    );
  },
  renderSequenceLevel: function() {
    return (
      React.createElement('div', {className: 'inner_con_banner'},
        React.createElement('div', {},
          React.createElement('div', {className: 'variation-bar-top sequenceComponent'},
            React.createElement('div', {className: 'variation-name-bar'},
              this.renderSequenceName(this.props.viewerRange[0], this.props.snp)
            ),
            React.createElement('div', {className: 'variation-pointer-top'},
                this.renderSequenceTopPointer(this.props.viewerRange[0],this.props.viewerRange[1], this.props.exon, this.props.snp)
              )
          ),
          React.createElement('div', {className: 'variation-bar-bottom sequenceComponent'},
            React.createElement('div', {className: 'variation-name-bar'},
              this.renderSequenceName(this.props.viewerRange[0], this.props.snp)
            ),
            React.createElement('div', {className: 'variation-pointer-bottom'},
                this.renderSequenceBottomPointer(this.props.viewerRange[0],this.props.viewerRange[1], this.props.exon, this.props.snp)
            )
          ),
          this.renderControlPanel()
        )
      )
    );
  },
  render: function() {
    var renderer;
    if (this.props.drillLevel == 0) { // Gene level
      renderer = this.renderGeneLevel();
    } else if (this.props.drillLevel == 1) { // Exon level
      renderer = this.renderExonLevel();
    } else if (this.props.drillLevel == 2) { // SNP level
      renderer = this.renderSequenceLevel();
    }
    return renderer;
  }
});
