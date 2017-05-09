#include "power_func.h"

#ifndef OPCODE_FUNC_H
#define OPCODE_FUNC_H

// clang-format off
#define LLVM_IR_Move 0
#define LLVM_IR_Ret 1
#define LLVM_IR_Br 2
#define LLVM_IR_Switch 3
#define LLVM_IR_IndirectBr 4
#define LLVM_IR_Invoke 5
#define LLVM_IR_Resume 6
#define LLVM_IR_Unreachable 7
#define LLVM_IR_CleanupReturnInst 8
#define LLVM_IR_CatchReturnInst 9
#define LLVM_IR_CatchSwitchInst 10
// end terminator insts
#define LLVM_IR_Add 11
#define LLVM_IR_FAdd 12
#define LLVM_IR_Sub 13
#define LLVM_IR_FSub 14
#define LLVM_IR_Mul 15
#define LLVM_IR_FMul 16
#define LLVM_IR_UDiv 17
#define LLVM_IR_SDiv 18
#define LLVM_IR_FDiv 19
#define LLVM_IR_URem 20
#define LLVM_IR_SRem 21
#define LLVM_IR_FRem 22
#define LLVM_IR_Shl 23
#define LLVM_IR_LShr 24
#define LLVM_IR_AShr 25
#define LLVM_IR_And 26
#define LLVM_IR_Or 27
#define LLVM_IR_Xor 28
#define LLVM_IR_Alloca 29
#define LLVM_IR_Load 30
#define LLVM_IR_Store 31
#define LLVM_IR_GetElementPtr 32
#define LLVM_IR_Fence 33
#define LLVM_IR_AtomicCmpXchg 34
#define LLVM_IR_AtomicRMW 35
#define LLVM_IR_Trunc 36
#define LLVM_IR_ZExt 37
#define LLVM_IR_SExt 38
#define LLVM_IR_FPToUI 39
#define LLVM_IR_FPToSI 40
#define LLVM_IR_UIToFP 41
#define LLVM_IR_SIToFP 42
#define LLVM_IR_FPTrunc 43
#define LLVM_IR_FPExt 44
#define LLVM_IR_PtrToInt 45
#define LLVM_IR_IntToPtr 46
#define LLVM_IR_BitCast 47
#define LLVM_IR_AddrSpaceCast 48
// funcletpad
#define LLVM_IR_CleanupPad 49
#define LLVM_IR_CatchPadInst 50
// end funcletpad
#define LLVM_IR_ICmp 51
#define LLVM_IR_FCmp 52
#define LLVM_IR_PHI 53
#define LLVM_IR_Call 54
#define LLVM_IR_Select 55
// useropt
#define LLVM_IR_UserOpt1 56
#define LLVM_IR_UserOpt2 57
// end useropt
#define LLVM_IR_VAArg 58
#define LLVM_IR_ExtractElement 59
#define LLVM_IR_InsertElement 60
#define LLVM_IR_ShuffleVector 61
#define LLVM_IR_ExtractValue 62
#define LLVM_IR_InsertValue 63
#define LLVM_IR_LandingPad 64
#define LLVM_IR_DMAFence 97
#define LLVM_IR_DMAStore 98
#define LLVM_IR_DMALoad 99
#define LLVM_IR_IndexAdd 100
#define LLVM_IR_SilentStore 101
#define LLVM_IR_Sine 102
#define LLVM_IR_Cosine 103
// clang-format on

std::string string_of_op(const int microop);

#endif
