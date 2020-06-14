var BannerComponent = React.createClass({
  getInitialState : function() {
    console.log(this.props.data);
    return {
      geneSequence: {
          chromosome: this.props.data.chromosome,
          chromosomeHighlighter: this.props.data.chromosomeHighlight,
          chrImgSrc: this.props.chrImgSrc,
          gene: this.props.data,
          exon: this.props.data.exon
      }
    };
  },
  handleResizeOnGene: function() {
    var parentWidth = Math.floor(jQuery('.inner_con_banner').width());
    var proportion = Math.floor(parentWidth/5); // 5 is 5px, the width of a pointer
    var geneSequence = this.state.geneSequence;
    this.setState({
        geneSequence: geneSequence
    });
  },
  sequenceLevel: function(k) {
    if (this.state.geneSequence.exon[k].hasOwnProperty('snps')) {
      if (this.state.geneSequence.exon[k].snps.length > 0) {
        var href = '/variation/'+this.state.geneSequence.exon[k].snps[0];
        window.location.href = href;
      }
    }
  },
  render: function() {
    return (
      React.createElement('div', {className: 'images_secs'},
        React.createElement(ChromosomeComponent, {
          chromosome: this.state.geneSequence.chromosome
        }),
        React.createElement(ChromosomeHighlighterComponent, {
          highlighter: this.state.geneSequence.chromosomeHighlighter,
          chrImgSrc: this.state.geneSequence.chrImgSrc
        }),
        React.createElement('img', {className: 'img-chrom-body ', src: this.props.imgSrc}),
        React.createElement(SequenceBrowserComponent, {
          gene: this.state.geneSequence.gene,
          exon: this.state.geneSequence.exon,
          // Funcs
          handleResizeOnGene: this.handleResizeOnGene,
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
      var cutChromName = this.props.chromosome.chromosomeId;
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
  // x. GENE BROWSER COMPONENT
  var SequenceBrowserComponent = React.createClass({
  propTypes: {
      gene: React.PropTypes.any,
      exon: React.PropTypes.any,
      handleResizeOnGene: React.PropTypes.func,
  },
  componentDidMount: function() {
    this.handleResizeOnGene();
    window.addEventListener('resize', this.handleResizeOnGene);
  },
  handleResizeOnGene: function () {
      this.props.handleResizeOnGene();
  },
  handleExonLevel: function(k) {
    this.props.exonLevel(k);
  },
  handleExonSequenceMoveNext: function() {
    var leftPos = jQuery('.exon-bar').scrollLeft();
    jQuery(".exon-bar").animate({scrollLeft: leftPos + 250}, 400);
  },
  handleExonSequenceMoveBack: function() {
    var leftPos = jQuery('.exon-bar').scrollLeft();
  	if (leftPos > 0) {
  			jQuery(".exon-bar").animate({scrollLeft: leftPos - 250}, 400);
  	}
  },
  handleSequenceLevel: function(k) {
    if (this.props.exon[k].variations.length > 0) {
      var href = '/variation/'+this.props.exon[k].variations[0];
      window.location.href = href;
    }
  },
  handleFilterExon: function(gene, exon) {
    var TYPE = {"exon": 1, "spaces": 2};
    // exon.sort(function(a,b) {
    //   var a_rank = parseInt(a.rank)
    //   var b_rank = parseInt(b.rank)
    //   if (a_rank < b_rank)
    //     return -1;
    //     if (a_rank > b_rank)
    //       return 1;
    //     return 0;
    // });
    ////////////////////////////////////////////////////////////////////////////
    // Scale
    var start = exon[0].start;
    var end = exon[exon.length-1].end;
    
    // New scaled exons
    var exonMap = [];
    
    for (var i = 0; i <= exon.length; i++) {
      if (exon[i]) {
        var e = exon[i];
        
        var point = Math.round((exon[i].end - exon[i].start) / 20);
        
        var numSnps = (e.hasOwnProperty('variations')) ? e.variations.length : 0;

        var exonMapItem = {
          index: i,
          name: e.name,
          point: parseInt(Math.abs(point)),
          numSnps: numSnps,
          color: ' light',
          gene: gene.name,
          rank: exon[i].rank,
          type: TYPE["exon"],
        }
        exonMap.push(exonMapItem);
        
        // Space among exons
        if (exon[i+1]) {
          var point = Math.round((exon[i+1].start - exon[i].end) / 20);
          var spaceItem = {
            name: "Spaced-Exon",
            point: parseInt(Math.abs(point)),            
            color: ' gray',            
            type: TYPE["spaces"],
          }
          exonMap.push(spaceItem);
        }
        
      }  
    }
    return exonMap;
  },
  //////////////////////////////////////////////////////////////////////////////
  // RENDER
  renderControlPanel: function () {
    return (
      React.createElement('div', {className: 'sequenceControlBtnGroup'},
        React.createElement('div', {className: 'rightGroup'},
          React.createElement('div', {className: 'viewlevel'}, 'Magnification level: Gene'),
          React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-left', onClick: this.handleExonSequenceMoveBack }),
  				React.createElement('div', {className: 'genPreBtn sequenceMovingControlBtn glyphicon glyphicon-triangle-right', onClick: this.handleExonSequenceMoveNext })
        )
      )
    );
  },

  renderExonPointer: function generatePointer(exonMap) {
    var elements = [];
    var mapping = ['Short', 'Med', 'Long', 'Long', 'Med', 'Short'];

    ////////////////////////////////////////////////////////////////////////////
    var pointerIndicate = 0;
    var randomPointer = 5;
    var index = 0;
    var root = this;
    
    ///////////////////////////////////
    exonMap.map(function(item) {
      for (var j = 1; j <= item.point; j++) {
        var attrGeneWrapper = {};
        attrGeneWrapper.className = 'gene-wrapper gene-wrapper-color';
        var attr = {};
        attr.className = 'exon-pointer pointer';
        attr.className = attr.className + ' icon-Gen'+mapping[pointerIndicate%6] + item.color;

        if (item.type == 1) {
          attr.onClick = root.handleSequenceLevel.bind(null, item.index);
          attr.title = ((item.numSnps > 0) ? item.numSnps.toString() : "0") + " variation(s) in this exon"; // Temperation
        }

        elements.push(
          React.createElement('div', {key: pointerIndicate, className: 'exon-sequence'},
              React.createElement('div', attrGeneWrapper,
                  React.createElement('div', attr)
              )
          )
        );
        pointerIndicate = pointerIndicate + 1;
      }
    });
    
    ///////////////////////////////////
    return elements;
  },
  renderExonName: function (exonMap, geneName) {
    var elements = [];
    var root = this;
    ////////////////////////////////////////////////////////////////////////////
    var tracker = 0;
    var index = 0;
    for (var i = 0; i < exonMap.length; i++) {
      if (exonMap[i].type == 1) {
        index += 1;
        var space = 0;
        if ((exonMap[i+1]) && (exonMap[i+1].type == 2)) {
          if (exonMap[i+1].point > 0) {
            space = (exonMap[i+1].point);
          }
        }

      	var position = ((tracker * 5)).toString()+'px';
      	tracker = tracker + (exonMap[i].point + space);
      	var attr = {};
        var color = ' light';
      	attr.style = {};
      	attr.style.marginLeft = position;
      	attr.style.display = 'inline';
      	attr.className = 'exonName' + exonMap[i].color;
      	attr.id = 'exon-'+i;
      	attr.key = i;
      	var exonName = "Exon" + " " + (index).toString();
      	elements.push(
      		React.createElement('div', attr, exonName)
      	);
      }
    }
    var attrGene = {};

    attrGene.className = 'topName';
    attrGene.style = {};
    attrGene.style.paddingLeft = '10px';
    attrGene.style.fontSize = '16px';
    attrGene.text = geneName;
    return (
        React.createElement('div',{},
          React.createElement('div', {},
    				React.createElement('span', attrGene, attrGene.text)
    			),
          elements
        )
    );
  },
  render: function() {
    var exonMap = this.handleFilterExon(this.props.gene, this.props.exon);
    var geneName = (this.props.gene.name != '') ? this.props.gene.name + ' gene' : '';
    return (
      React.createElement('div', {className: 'inner_con_banner'},
        React.createElement('div', {},
          React.createElement('div', {className: 'exon-bar-top exon-bar'},
            React.createElement('div', {className: 'sequenceGenesName'},
              this.renderExonName(exonMap, geneName)
            ),
            React.createElement('div', {className: 'exon-pointer-top'},
                this.renderExonPointer(exonMap)
              )
          ),
          React.createElement('div', {className: 'exon-bar-bottom exon-bar'},
            React.createElement('div', {className: 'sequenceGenesName'},
              this.renderExonName(exonMap)
            ),
            React.createElement('div', {className: 'exon-pointer-bottom'},
                this.renderExonPointer(exonMap, geneName)
            )
          ),
          this.renderControlPanel()
        )
      )
    );
  }
});
