var BannerComponent = React.createClass({
  getInitialState : function() {
    return {
      indexLetter: 0,
      chromosome: this.props.data.chromosome,
      chromosomeHighlighter: this.props.data.chromosomeHighlight,
      bodyHighlighter: this.props.data.bodyHighlight,
      geneSequence: {
        viewerLength: 20,
        viewerRange: [0, 116],
        chromosome: this.props.data,
        gene: this.props.data.gene,
        exon: this.props.data.exon,
        snp: this.props.data.snp
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
  justifyPosition: function(data) {
    var left_position = parseInt(jQuery('#snpName').css('margin-left').replace('px', ''));
    var distance = Math.ceil((left_position)-(left_position/6));
    var leftPos = jQuery('.variation-bar').scrollLeft();
    jQuery(".variation-bar").animate({scrollLeft: leftPos + (distance)}, 0);
  },
  sequenceLevel: function(k) {
    if (this.state.geneSequence.exon[k].hasOwnProperty('snps')) {
      if (this.state.geneSequence.exon[k].snps.length > 0) {
        var href = '/variation/'+this.state.geneSequence.exon[k].snps[0];
        window.location.href = href;
      }
    }
  },
  exonLevel: function(k) {
    var href = '/gene/'+this.state.geneSequence.gene.geneId;
    window.location.href = href;
  },
  zoomIn: function() {
    // Hide
  },
  zoomOut: function() {
    this.exonLevel(0);
  },
  render: function() {
      var styleImageSecs= { minHeight: '700px', maxHeight: '750px'};
    return (
      React.createElement('div', {className: 'images_secs', style: styleImageSecs},
      React.createElement(ChromosomeHighlighterComponent, { highlighters: this.state.chromosomeHighlighter }),
      React.createElement(BodyHighlighterComponent, { highlighters: this.state.bodyHighlighter }),
      React.createElement('img', {className: 'img-chrom-body ', src: this.props.imgSrc})
      )
    );
  }
});
/////////////////////////////////////////
// x. CHROMOSOME HIGHLIGHTER COMPONENT
var ChromosomeHighlighterComponent = React.createClass({
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
          var connectorText = 'connector-organ-'+h.position;
            var contentText = 'connector-text-organ-'+h.position;
          return (
              React.createElement('div', {key: i},
                React.createElement('div', {className: connectorText}),
                  React.createElement('div', {className: contentText, title: h.text}, h.text)
            )
          );
        })
      )
    );
  }
});
