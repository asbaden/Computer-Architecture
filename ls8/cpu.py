"""CPU functionality."""
import sys
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.sp = 7
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.return_pc = 0 
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.ADD = 0b10100000
    def load(self, program):
        """Load a program into memory."""
        #    index     value        provide from arg
        for address, instruction in enumerate(program):
            self.ram[address] = instruction
            print(address, bin(instruction))
            address += 1
    def alu(self, op, reg_a = 0, reg_b = 1):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            print("REGISTRY:", self.reg)
            self.pc += 3
            return self.reg[reg_a]
        else:
            raise Exception(f"Unsupported ALU operation: {op}")
            self.trace()
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    def run(self):
        """Run the CPU.
        1. read mem at PC
        2. store result in local var
        """
        running = True
        self.reg[self.sp] = 0xf3

        while running:
            IR = self.ram[self.pc]
            if IR == self.LDI:
                self.ldi()
            if IR == self.PRN:
                self.prn()           
            if IR == self.MUL:
                self.alu("MUL", 0, 1)
            if IR == self.HLT:
                running = self.hlt()
            if IR == self.POP:
                self.pop()
            if IR == self.PUSH:
                self.push()
            if IR == self.CALL:
                self.call()
            if IR == self.RET:
                self.ret()
            if IR == self.ADD:
                self.add()
    def ram_read(self, address):
        # accept address
        # return it's value
        return self.ram[address]
    def ram_write(self, value, address):
        # take a value
        # write to address
        # no return
        self.ram[address] = value
    def hlt(self):
        self.pc += 1 
        return False
    def prn(self):
        reg_id = self.ram[self.pc + 1]
        self.reg[0]
        print("Returning", self.reg[reg_id])
        self.pc +=2
    def ldi(self):
        reg_id = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[reg_id] = value
        self.pc += 3
    
    def add(self):
        reg_a = 0
        reg_b = 0
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3
    
    def push(self):
        self.reg[self.sp] -= 1
        reg_id = self.ram[self.pc +1]
        # print("this is pc", self.pc)
        value = self.reg[reg_id]
        top_loc = self.reg[self.sp]
        self.ram[top_loc] = value
        print("RAM", self.ram)
        print("REG", self.reg)
        self.pc += 2 
    def pop(self):
        # old head
        top_loc = self.reg[self.sp]
        print("this is self.sp", self.sp)
        # lets get the register address
        # new head
        reg_addr = self.ram[self.pc + 1]
        print("this is reg address", reg_addr)
        # overwrite our reg address with the value of our memory address we are looking at
        self.reg[reg_addr] = self.ram[top_loc]
        self.reg[self.sp] += 1
        self.pc += 2
    
    def call(self):
        # 1. The address of the ***instruction*** _directly after_ `CALL` is
        # pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        # 2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.
        # where we're going to RET
       
        return_pc = self.pc + 2
        
       
        # print("return_pc", retun_pc)
        # print("value in ram", self.reg[reg_address])
        
        #push on the stack 
        self.reg[self.sp] -= 1
        top_loc = self.reg[self.sp]
        self.ram[top_loc] = return_pc
        

        subroutine_pc = self.reg[1]

        #call it 
        self.pc = subroutine_pc
    
    def ret(self):
        print("REG in RET", self.reg)
        print("RAAAM", self.ram)
        # Return from subroutine.
        top_of_stack_address = self.reg[self.sp]
        reg_address = self.ram[top_of_stack_address]
        self.pc = reg_address
        # Pop the value from the top of the stack and store it in the `PC`.




