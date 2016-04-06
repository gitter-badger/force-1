require('menu.css');

var DropdownButton = require('react-bootstrap').DropdownButton;
var MenuItem = require('react-bootstrap').MenuItem;
var Category = require('./Category');
var Input = require('react-bootstrap').Input;
var Menu = React.createClass({
    render: function() {
        return (
            <div className="menu">
                Меню на <DropdownButton bsStyle="link" title="понедельник" eventKey={1} id="0">
                <MenuItem eventKey={0}>понедельник</MenuItem>
                <MenuItem eventKey={1}>вторник</MenuItem>
                <MenuItem eventKey={2}>среду</MenuItem>
                <MenuItem eventKey={3}>четверг</MenuItem>
                <MenuItem eventKey={4}>пятницу</MenuItem>
                <MenuItem eventKey={5}>субботу</MenuItem>
                <MenuItem eventKey={6}>воскресенье</MenuItem>
                </DropdownButton>
                {
                    this.props.products.map(function(category){
                        return (<Category key={category[0]}
                                          value={category[1]}
                                          products={category[2]}/>);
                    })
                }
            </div>
        )
    }
});

module.exports = Menu;
