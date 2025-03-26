from src.protocols.ICookAction import ICookAction
from src.protocols.IHandOrderToCustomerAction import IHandOrderToCustomerAction
from src.protocols.IMoveAction import IMoveAction
from src.protocols.INotifyKitchenAction import INotifyKitchenAction
from src.protocols.IPickUpOrderAction import IPickUpOrderAction
from src.protocols.ISeatAction import ISeatAction
from src.protocols.ITakeOrderAction import ITakeOrderAction
from src.protocols.IWaitAction import IWaitAction


IAction = ICookAction | ISeatAction | IMoveAction | ITakeOrderAction | INotifyKitchenAction | IHandOrderToCustomerAction | IWaitAction | IPickUpOrderAction