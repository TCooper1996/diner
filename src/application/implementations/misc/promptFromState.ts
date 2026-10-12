import { RestaurantState } from '@core/models/RestaurantState';

/**
 * Convert the current game state to a JSON string for use in prompts
 */
export function toPrompt(state: RestaurantState): string {
    const orders = state.orders.getAllOrders();
    const employees = state.employees.getAllEmployees();
    const customers = state.customers.getAllCustomers();
    
    const employeeDict: Record<string, any> = {};
    
    for (const e of employees) {
        const ordersTaken = state.employeeOrders.getOrdersTaken(e.name);
        const ordersBeingCarried = state.employeeOrders.getOrdersCarried(e.name);
        
        employeeDict[e.name] = {
            name: e.name,
            orders_taken: ordersTaken,
            orders_being_carried: ordersBeingCarried,
        };
    }
    
    const customerDict: Record<string, any> = {};
    for (const c of customers) {
        let customerOrder = '';
        try {
            const orderId = state.customerOrders.getOrderOfCustomer(c.id);
            customerOrder = orderId;
        } catch (e) {
            // Customer may not have an order
        }
        
        customerDict[c.name] = {
            name: c.name,
            status: c.status,
            orders: customerOrder,
        };
    }
    
    const stateObj = {
        employees: employeeDict,
        customers: customerDict,
        orders: Object.fromEntries(
            orders.map(o => [
                `#${o.id}`, 
                { 
                    status: o.status, 
                    "order#": o.id 
                }
            ])
        ),
    };
    
    return JSON.stringify(stateObj, null, 4);
} 