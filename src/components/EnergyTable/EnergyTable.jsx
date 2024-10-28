import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

const invoices = [
    {
        month: "Daikin_1_0",
        paymentStatus: "1 / 12",
        totalAmount: "14 hp",
        paymentMethod: "Cooling Only",
    },
    {
        month: "Daikin_1_0",
        paymentStatus: "1 / 12",
        totalAmount: "14 hp",
        paymentMethod: "Cooling Only",
    },
    {
        month: "Daikin_1_0",
        paymentStatus: "1 / 12",
        totalAmount: "14 hp",
        paymentMethod: "Cooling Only",
    },
    {
        month: "Daikin_1_0",
        paymentStatus: "1 / 12",
        totalAmount: "14 hp",
        paymentMethod: "Cooling Only",
    },
    {
        month: "Daikin_1_0",
        paymentStatus: "1 / 12",
        totalAmount: "14 hp",
        paymentMethod: "Cooling Only",
    },
    {
        month: "Daikin_1_0",
        paymentStatus: "1 / 12",
        totalAmount: "14 hp",
        paymentMethod: "Cooling Only",
    },
    {
        month: "Daikin_1_0",
        paymentStatus: "1 / 12",
        totalAmount: "14 hp",
        paymentMethod: "Cooling Only",
    },
]

export function EnergyTable() {
    return (
        <Table className="">
            {/* <TableCaption>A list of your recent invoices.</TableCaption> */}
            <TableHeader>
                <TableRow className="bg-gray-300">
                    <TableHead className="w-[100px]">System</TableHead>
                    <TableHead className="text-center">ODU(4) / IDU(50)</TableHead>
                    <TableHead className="text-center">Type</TableHead>
                    <TableHead className="text-right">Capacity</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {invoices.map((invoice) => (
                    <TableRow key={invoice.invoice}>
                        <TableCell className="font-medium">{invoice.month}</TableCell>
                        <TableCell className="text-center">{invoice.paymentStatus}</TableCell>
                        <TableCell className="text-center">{invoice.paymentMethod}</TableCell>
                        <TableCell className="text-right">{invoice.totalAmount}</TableCell>
                    </TableRow>
                ))}
            </TableBody>
            <TableFooter>
                <TableRow>
                    <TableCell colSpan={3}>Total</TableCell>
                    <TableCell className="text-right">180 hp</TableCell>
                </TableRow>
            </TableFooter>
        </Table>
    )
}