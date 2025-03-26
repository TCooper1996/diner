from src.actions.cook import CookAction, cook_food
from src.state.employee.employee import Employee
from src.state.game import GameState
from src.state.order import Order, OrderStatus


def test_cook():
    
    """Test that a cook prepares food for pending orders"""
    # Create a cook with instructions to prepare food
    cook = Employee(name="Bob", instruction="Your job is to cook food", location="kitchen")
    order = Order(customer_id="1", items=["burger"], status=OrderStatus.SUBMITTED, server="Bob")
    game = GameState(employees={cook.name: cook}, orders={order.id: order})

    # Test normal flow

    # Process the cook's turn
    action = CookAction(order_id=order.id)
    result = cook_food(cook, game, action)

    # Check that the order's status has changed to READY
    assert result.success
    assert result.game_state.grab_order(order.id).status == OrderStatus.READY
    
    # Test that an order cant be cooked twice
    result2 = cook_food(cook, result.game_state, action)
    assert not result2.success
    assert result2.game_state == result.game_state


    # Test that cook must be in kitchen
    cook.location = "dining"

    result = cook_food(cook, game, action)
    assert not result.success



