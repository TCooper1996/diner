
export interface EmployeeKitchenTerminalRepo {
  getEmployeeKitchenTerminal(employeeId: string): string | null;
  addEmployeeKitchenTerminal(employeeId: string, kitchenTerminalId: string): void;
  removeEmployeeKitchenTerminal(employeeId: string): void;
}
