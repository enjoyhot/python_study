var React = require("react");
var ReactDOM = require("react-dom");
var LineChart = require("react-chartjs").Line;



var chartData = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90]
        }
    ]
};

var chartOptions = {};


var MyComponent = React.createClass({
  render: function() {
    return <LineChart data={chartData} options={chartOptions} width="880" height="250"/>
  }
});

ReactDOM.render(
  <MyComponent />,
  document.getElementById('content')
);


// form

var FormComp = React.createClass({

    // To get rid of those input refs I'm moving those values
    // and the form message into the state
    getInitialState: function() {
        return {
            name: '',
            email: '',
            message: ''
        };
    },

    handleSubmit: function(e) {
        e.preventDefault();
        var userName = this.state.name.trim();
        var userEmail = this.state.email.trim();
        if(!userName || !userEmail) return;
        this.setState({
            name: '',
            email: '',
            message: 'Please wait...'
        });


        this.props.onFormSubmit({
            userName: userName, 
            userEmail: userEmail
            }, function(data) {
                this.setState({ message: data.msg });
            });
    },

    changeName: function(e) {
        this.setState({
        name: e.target.value
        });
    },

    changeEmail: function(e) {
        this.setState({
            email: e.target.value
        });
    },

  render: function() {
    // the message and the input values are all component state now
    return (
      <div>
        <div className="result">{ this.state.message }</div>
                <form class="form form-vertical" onSubmit={ this.handleSubmit }>                    
                    <div class="control-group">
                        <label>Name</label>
                        <div class="controls">
                            <input type="text" class="form-control" name="userName" value={ this.state.name } onChange={ this.changeName }  placeholder="Enter Name" />
                        </div>
                    </div>
                    <div class="control-group">
                        <label>Message</label>
                        <div class="controls">
                            <input class="form-control" name="userEmail" value={ this.state.email } onChange={ this.changeEmail } placeholder="Enter Name" />
                        </div>
                    </div>
                    <div class="control-group">
                        <label></label>
                        <div class="controls">
                            <button type="submit" class="btn btn-primary">
                                Post
                            </button>
                        </div>
                    </div>
                </form>
      </div>
    );
  }

});

var RC = React.createClass({
    onFormSubmit: function(data, callback){
        $.ajax({
            url:"/cls/logistic/post",
            dataType: 'json',
            type: 'POST',
            data: data,
            success: callback,
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function() {
        return <FormComp onFormSubmit={this.onFormSubmit} />
    }
});

ReactDOM.render(
    <RC />,
    document.getElementById('logistic-form')
);