from src.actions.hand_order_to_customer import HandOrderToCustomer, hand_food_to_customer
from src.state.customer import Customer, CustomerStatus
from src.state.employee.employee import Employee
from src.state.game import GameState
from src.state.order import Order, OrderStatus


def test_hand_order_to_customer():
    order_id = "1"

    e = Employee(name="Alice", instruction="Your job is to deliver food to customers", location="dining")
    cust = Customer(id="1", location="dining", status=CustomerStatus.ORDERED, order_id=order_id)
    order = Order(order_id=order_id, customer_id="1", items=["burger"], status=OrderStatus.READY)

    order_carriers = {e.name: [order_id]}
    order_takers = {e.name: [order_id]}
    game = GameState(employees={e.name: e}, customers={cust.id: cust}, orders={order.id: order}, order_carriers=order_carriers, order_takers=order_takers)

    

    assert len(game.orders_carried_by_employee(e.name)) == 1

    action = HandOrderToCustomer(order_id=order.id, customer_id=cust.id)
    result = hand_food_to_customer(e, game, action)
    assert result.success
    # Order status updated
    assert result.game_state.grab_order(order.id).status == OrderStatus.DELIVERED
    # Customer is eating
    assert result.game_state.grab_customer(cust.id).status == CustomerStatus.EATING
    # Server no longer holds food
    assert len(result.game_state.orders_carried_by_employee(e.name)) == 0


    # Ensure food is in inventory


