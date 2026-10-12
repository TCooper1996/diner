import { Customer } from '@core/entities/Customer';
import { CustomerRepo } from '@core/repos/CustomerRepo';

/**
 * Implementation of the CustomerRepo interface that stores customers in a Map.
 */
export class CustomerRepoImpl implements CustomerRepo {
    private customers: Map<string, Customer>;

    constructor() {
        this.customers = new Map<string, Customer>();
    }

    getAllCustomers(): Customer[] {
        return Array.from(this.customers.values());
    }

    getCustomer(customerId: string): Customer {
        const customer = this.customers.get(customerId);
        if (!customer) {
            throw new Error(`No customer found with ID ${customerId}`);
        }
        return customer;
    }

    getCount(): number {
        return this.customers.size;
    }

    addCustomer(customer: Customer): void {
        if (this.customers.has(customer.id)) {
            throw new Error(`Customer with ID ${customer.id} already exists`);
        }
        this.customers.set(customer.id, customer);
    }

    updateCustomer(customer: Customer): void {
        if (!this.customers.has(customer.id)) {
            throw new Error(`No customer found with ID ${customer.id} to update`);
        }
        this.customers.set(customer.id, customer);
    }
} 