var UserComponent = React.createClass({
  getInitialState: function() {
    return (
      {
        labUser:false,
      }
    );
  },
  componentDidMount: function() {
    this.handleLoadLabUser();
  },
  handleLogout:function(){
    setCookie('token','',-1);
    location.reload();
      
  },
  handleLoadLabUser:function () {
    accessToken = getCookie('token');
    this.serverRequest = jQuery.post(LAB_NETWORK_API+'/api/loadLabUser', JSON.stringify({token:accessToken}),function (data) {
      if (data['code']=='200') {
        this.setState({labUser:true});
      }
    }.bind(this));
  },
  renderRightButton:function(){
    var href = window.location.href;
    
    if (href.match(/\/labOfferList$/gi)) {
      return (
        React.createElement('a', {className: 'btn-s-blue clickable', 'href':"/genebay"}, "Back to gene bay")
      );
    }
    if (href.match(/\/labQuestionList/gi)) {
      return (
        React.createElement('a', {className: 'btn-s-blue clickable', 'href':"/labOfferList"}, "Back to offer list")
      );
    }
    return (
        React.createElement('a', {className: 'btn-s-blue clickable', 'href':"/labOfferList"}, "View Your Offers")
    );
  
  },
  render: function(){
      if (!this.state.labUser) {
        return(
          
          React.createElement('div', {className: 'userBlock'},
            React.createElement('a', {className: 'btn-s-green clickable', 'data-toggle':"modal", 'data-target':"#signinLabM" }, "Login"),
            React.createElement('a', {className: 'btn-s-blue clickable', 'data-toggle':"modal", 'data-target':"#signupLabM"}, "Register")
          )
        );   
      }

      return(
          React.createElement('div', {className: 'userBlock'},
            React.createElement('a', {
              className: 'btn-s-green clickable',
              onClick: this.handleLogout,
              },"Logout"),
            this.renderRightButton()
          )
       );  
  }
  
});