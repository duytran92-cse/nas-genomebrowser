var LabQuestionForm = React.createClass({
    getInitialState: function() {
        return ({
            offerForm: [],

        });
    },
    componentDidMount: function() {
        var root = this;
        jQuery('#questionForm #idQuestion').change(function() {
            idQuestion = jQuery(this).val();
            root.handleLoadForm(idQuestion);
        });

        jQuery('#questionForm #question-form-submit').click(function() {
            root.handleSubmitForm();
        });

    },
    handleLoadForm: function(idQuestion = '') {
        
        var root = this;
        var sendData = {};
        sendData['token'] = getCookie('token');
        sendData['idQuestion'] = idQuestion;
        jQuery.ajax({
            url: LAB_NETWORK_API + '/api/labQuestionForm',
            data: sendData,
            method: 'GET',
        }).done(function(result) {
            if (result['code'] == 100) {
                jQuery("#labQuestionForm").html(result['error']);
            } else if (result['code'] == 200) {
                root.setState({
                    offerForm: result['form']
                });
                
            }
        });
    },
    handleSubmitForm: function() {
        $ = jQuery;
        var form = $('#questionForm');
        
        $('.form-control.required',form).each(function(){
            if ($(this).val()=="") {
                $(this).css('border-color','red');
                return false;
            }
            $(this).attr('style','');
        });
        
        var message = jQuery("#mess-question-form",form);
        var idQuestion = jQuery("#idQuestion",form).val();
    
        var formData = new FormData();
        formData.append('idQuestion', idQuestion);
        formData.append('token',  getCookie('token'));

        $('.form-group',form).each(function(){
            $('textarea,input[type="text"],input[type="number"]',this).each(function(){
                formData.append($(this).attr('name'), $(this).val());        
            });
        });
        
        $.ajax({
            type: "post",
            dataType: 'json',
            url:  LAB_NETWORK_API + '/api/labQuestionFormSubmit',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['code'] == 100) {
                   jQuery("#labQuestionForm").html(result['error']);
                } else if (result['code'] == 200) {
                    if (result['mailStatus'] =='Mail sent') {
                        message.html(result['mailStatus']).attr('style', 'color: green');
                    } else {
                        message.html(result['mailStatus']).attr('style', 'color: red');
                    }
                    jQuery('#questionListReloadElement').trigger('change');
                }
            },
            error: function (result) {
                console.log(result);
                message.html('Form submit failed. Please try again!').attr('style', 'color: red');
            }
        });     

    },
    handleChange:function(event){
        offerForm = this.state.offerForm;
        for (i in offerForm){
            if (offerForm[i].name == event.target.id) {
                offerForm[i].defaultValue = event.target.value;
            }
        }
        this.setState({
            offerForm: offerForm
        });  
    },

    renderFormItems: function() {
        var items = [];
        var root = this;
        this.state.offerForm.map(function(i, k) {
            requiredText = '';
            requiredClass = '';
            if (i.required) {
                requiredText = ' *';
                requiredClass = 'required';
            }
            switch (i.type) {
                case 'text':
                case 'number':
                    var element = React.createElement('input', {
                            type: i.type,
                            name: i.name,
                            className: 'form-control shadow no-radius ' + requiredClass,
                            required:requiredClass,
                            id: i.name,
                            value: i.defaultValue,
                            onChange:root.handleChange,
                        }

                    );
                    break;
                case 'textarea':
                    var element = React.createElement('textarea', {
                            name: i.name,
                            className: 'form-control shadow no-radius ' + requiredClass,
                            required:requiredClass,
                            id: i.name,
                            value: i.defaultValue,
                            onChange:root.handleChange,
                            rows:20
                        }

                    );
                    break;
                case 'label':
                    var element = React.createElement('div', {
                            name: i.name,
                            className: ' ',
                            id: i.name,
                        },
                        i.defaultValue
                    );
                    break;
                default:
                    element = '';

            }
            items.push(
                React.createElement('div', {
                        className: 'form-group'
                    },
                    React.createElement('label', {
                            'htmlFor': i.name
                        },
                        React.createElement('span', {}, i.title),
                        React.createElement('span', {
                            className: 'red'
                        }, requiredText)
                    ),
                    element
                )
            );
        });
        return items;
    },
    render: function() {
        return (
            React.createElement('div', {
                    className: 'form-container'
                },
                this.renderFormItems()
            )
        );
    }

})