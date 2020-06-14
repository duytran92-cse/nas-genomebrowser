var LabOfferForm = React.createClass({
    getInitialState: function() {
        return ({
            offerForm: [],

        });
    },
    componentDidMount: function() {
        var root = this;
        jQuery('#offerForm #idOffer').change(function() {
            idOffer = jQuery(this).val();
            root.handleLoadForm(idOffer);
        });

        jQuery('#offerForm #offer-form-submit').click(function(e) {
            root.handleSubmitForm();
            return false;
        });

    },
    handleLoadForm: function(idOffer = '') {
        
        var root = this;
        var sendData = {};
        sendData['token'] = getCookie('token');
        sendData['idOffer'] = idOffer;
        
        this.setState({
            offerForm: []
        });  
        jQuery.ajax({
            url: LAB_NETWORK_API + '/api/labOfferForm',
            data: sendData,
            method: 'GET',
        }).done(function(result) {
            if (result['code'] == 100) {
                jQuery("#labOfferForm").html(result['error']);
            } else if (result['code'] == 200) {
                root.setState({
                    offerForm: result['form']
                });
                root.handleSelect2();
            }
        });
    },
    handleSubmitForm: function() {
        $ = jQuery;
        var form = $('#offerForm');
        var message = jQuery("#mess-offer-form",form);  
       
       
        //validate
        var validate = true;
        $('.form-control.required',form).each(function(){
                if ($(this).val()==""|| $(this).val()==null) {
                    $(this).closest('.form-group').addClass('required');
                    validate = false;
                }else{
                    $(this).closest('.form-group').removeClass('required');
                }
            
        });
        if(parseInt($('#tatFrom',form).val())>=parseInt($('#tatTo',form).val())) {
            $('#tatFrom,#tatTo',form).css('border-color','red');
            message.html('Turn around time from  must be less than turn around time to').attr('style', 'color: red');
            validate = false;
        } else{
            message.html('').attr('style','');
            $('#tatFrom,#tatTo',form).attr('style','');
        }
        if (!validate) {
            return false;
        }
     

        //Submit
        var idOffer = jQuery("#idOffer",form).val();
    
        var formData = new FormData();
        formData.append('idOffer', idOffer);
        formData.append('token',  getCookie('token'));

        $('.form-group',form).each(function(){
            $('select,input[type="text"],input[type="number"]',this).each(function(){
                formData.append($(this).attr('name'), $(this).val());        
            });
        });
        
     
        $.ajax({
            type: "post",
            dataType: 'json',
            url:  LAB_NETWORK_API + '/api/labOfferFormSubmit',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['code'] == 100) {
                    jQuery("#labOfferForm").html(result['error']);
                } else if (result['code'] == 200) {
                   jQuery('#offerForm').modal('hide');
                   jQuery('#offerListReloadElement').trigger('change');
                }
            },
            error: function (result) {
                message.html('Form submit failed. Please try again!').attr('style', 'color: red');
            }
        });        
    

    },
    handleChange:function(event){
        offerForm = this.state.offerForm;
        offerForm[i].defaultValue = $('#labOfferForm #'+offerForm[i].name).val();
        this.setState({
            offerForm: offerForm
        });  
    },

    renderFormItems: function() {
        var items = [];
        var root = this;
        this.state.offerForm.map(function(i, k) {
            var requiredText = '';
            var requiredClass = '';
            if (i.required) {
                requiredText = ' *';
                requiredClass = 'required';
            }
            switch (i.type) {
                case 'text':
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
                case 'label':
                    var element = React.createElement('div', {
                            name: i.name,
                            className: '',
                            id: i.name,
                        },
                        i.defaultValue
                    );
                    break;
                case 'select':
                    var options = [];

                    for (option in i.options) {
                        options.push(
                            React.createElement('option', {
                                value: option
                            }, i.options[option])
                        );
                    };

                    var element = React.createElement('select', {
                            type: i.type,
                            name: i.name,
                            className: 'form-control shadow no-radius ' + requiredClass,
                            value: i.defaultValue,
                            onChange:root.handleChange,
                            id: i.name,
                            multiple: i.multiple,
                        },
                        options
                    );
                    break;
                case 'select2':
                    var options = [];
                    
                    for (option in i.options) {
                        options.push(
                            React.createElement('option', {
                                value: option
                            }, i.options[option])
                        );
                    };
                    var element = React.createElement('div', {},
                        React.createElement('select', {
                                name: i.name,
                                className: 'form-control shadow no-radius select2 ' + requiredClass,
                                value: i.defaultValue,
                                onChange:root.handleChange,
                                data: i.ajax,
                                multiple: i.multiple,
                                id: i.name,
                            },
                            options
                        )
                    );
                    break;
                default:
                    var element = '';

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
    handleSelect2: function() {
        $ = jQuery;
        $('select.select2').each(function() {
            var attr = JSON.parse($(this).attr('data'));
            var url = LAB_NETWORK_API + '/api/autocomplete';
            $(this).select2({
                ajax: {
                    url: url,
                    dataType: 'json',
                    data: function(input) {
                        return {
                            q: input.term,
                            params: attr
                        }
                    },
                    processResults: function(data, params) {
                        params.page = params.page || 1;
                        var parseResults = [];
                        for (index in data) {
                            parseResults.push({
                                'id': index,
                                'text': data[index],
                            });
                        }
                        return {
                            results: parseResults,
                            pagination: {
                                more: (params.page * 30) < data.total_count
                            }
                        };
                    },
                }
            });
        });
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