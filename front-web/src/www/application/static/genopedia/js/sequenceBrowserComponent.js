var SequenceBrowser = React.createClass({
    getInitialState: function() {
        var viewerRangeArr = [[0, 371], [0, 295], [0, 116]];
        var viewerLengthArr = [100, 60, 20];

        return {
            showSNPName: true,
            indexLetter: 0,
            chromosome: this.props.data.chromosome,
            chromosomeHighlighter: this.props.data.chromosomeHighlighter,
            geneSequence: {
                drillLevel: this.props.drillLevel,
                viewerLength: viewerLengthArr[this.props.drillLevel],
                viewerRange: viewerRangeArr[this.props.drillLevel],
                chromosome: this.props.data,
                gene: this.props.data,
                exon: this.props.data.exon,
                snp: this.props.data
            }
        }
    },

    componentDidMount: function() {

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

    moveSequencePrevious: function() {        
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
      
    },
    exonLevel: function(k) {
        window.location.href = '/gene/'+this.state.geneSequence.gene;
    },
    sequenceLevel: function(k) {
        if (this.state.geneSequence.exon[k].snps.length > 0) {
            window.location.href = '/variation/'+this.state.geneSequence.exon[k].snps[0];
        }
    },
    toggleShowSNPName: function() {
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
        } 
        else if (geneSequence.drillLevel == 1) {
            this.sequenceLevel(0)
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
        return (
            React.createElement('div', { className: 'images_sec' })
        );
    }

});