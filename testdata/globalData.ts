export class GlobalData {
    private static instance: GlobalData;
    private data: Map<string, any>;

    private constructor() {
        this.data = new Map<string, any>();
    }

    public static getInstance(): GlobalData {
        if (!GlobalData.instance) {
            GlobalData.instance = new GlobalData();
        }
        return GlobalData.instance;
    }

    // Set any value
    public setValue(key: string, value: any): void {
        this.data.set(key, value);
    }

    // Get any value
    public getValue(key: string): any {
        return this.data.get(key);
    }

    // Clear all data
    public clearAll(): void {
        this.data.clear();
    }
}