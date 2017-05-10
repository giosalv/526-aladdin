#include "opcode_func.h"

std::string string_of_op(const int microop) {
  switch (microop) {
  case LLVM_IR_Move :               return "Move";
  case LLVM_IR_Ret :                return "Ret";
  case LLVM_IR_Br :                 return "Br";
  case LLVM_IR_Switch :             return "Switch";
  case LLVM_IR_IndirectBr :         return "IndirectBr";
  case LLVM_IR_Invoke :             return "Invoke";
  case LLVM_IR_Resume :             return "Resume";
  case LLVM_IR_Unreachable :        return "Unreachable";
#ifdef GENERALIZED_TRACE
  case LLVM_IR_CleanupReturnInst :  return "CleanupReturnInst";
  case LLVM_IR_CatchReturnInst :    return "CatchReturnInst";
  case LLVM_IR_CatchSwitchInst :    return "CatchSwitchInst";
#endif
  case LLVM_IR_Add :                return "Add";
  case LLVM_IR_FAdd :               return "FAdd";
  case LLVM_IR_Sub :                return "Sub";
  case LLVM_IR_FSub :               return "FSub";
  case LLVM_IR_Mul :                return "Mul";
  case LLVM_IR_FMul :               return "FMul";
  case LLVM_IR_UDiv :               return "UDiv";
  case LLVM_IR_SDiv :               return "SDiv";
  case LLVM_IR_FDiv :               return "FDiv";
  case LLVM_IR_URem :               return "URem";
  case LLVM_IR_SRem :               return "SRem";
  case LLVM_IR_FRem :               return "FRem";
  case LLVM_IR_Shl :                return "Shl";
  case LLVM_IR_LShr :               return "LShr";
  case LLVM_IR_AShr :               return "AShr";
  case LLVM_IR_And :                return "And";
  case LLVM_IR_Or :                 return "Or";
  case LLVM_IR_Xor :                return "Xor";
  case LLVM_IR_Alloca :             return "Alloca";
  case LLVM_IR_Load :               return "Load";
  case LLVM_IR_Store :              return "Store";
  case LLVM_IR_GetElementPtr :      return "GetElementPtr";
  case LLVM_IR_Fence :              return "Fence";
  case LLVM_IR_AtomicCmpXchg :      return "AtomicCmpXchg";
  case LLVM_IR_AtomicRMW :          return "AtomicRMW";
  case LLVM_IR_Trunc :              return "Trunc";
  case LLVM_IR_ZExt :               return "ZExt";
  case LLVM_IR_SExt :               return "SExt";
  case LLVM_IR_FPToUI :             return "FPToUI";
  case LLVM_IR_FPToSI :             return "FPToSI";
  case LLVM_IR_UIToFP :             return "UIToFP";
  case LLVM_IR_SIToFP :             return "SIToFP";
  case LLVM_IR_FPTrunc :            return "FPTrunc";
  case LLVM_IR_FPExt :              return "FPExt";
  case LLVM_IR_PtrToInt :           return "PtrToInt";
  case LLVM_IR_IntToPtr :           return "IntToPtr";
  case LLVM_IR_BitCast :            return "BitCast";
  case LLVM_IR_AddrSpaceCast :      return "AddrSpaceCast";
#ifdef GENERALIZED_TRACE
  case LLVM_IR_CleanupPad :         return "CleanupPad";
  case LLVM_IR_CatchPadInst :       return "CatchPadInst";
#endif
  case LLVM_IR_ICmp :               return "ICmp";
  case LLVM_IR_FCmp :               return "FCmp";
  case LLVM_IR_PHI :                return "PHI";
  case LLVM_IR_Call :               return "Call";
  case LLVM_IR_Select :             return "Select";
#ifdef GENERALIZED_TRACE
  case LLVM_IR_UserOpt1 :           return "UserOpt1";
  case LLVM_IR_UserOpt2 :           return "UserOpt2";
#endif
  case LLVM_IR_VAArg :              return "VAArg";
  case LLVM_IR_ExtractElement :     return "ExtractElement";
  case LLVM_IR_InsertElement :      return "InsertElement";
  case LLVM_IR_ShuffleVector :      return "ShuffleVector";
  case LLVM_IR_ExtractValue :       return "ExtractValue";
  case LLVM_IR_InsertValue :        return "InsertValue";
  case LLVM_IR_LandingPad :         return "LandingPad";
  case LLVM_IR_DMAFence :           return "DMAFence";
  case LLVM_IR_DMAStore :           return "DMAStore";
  case LLVM_IR_DMALoad :            return "DMALoad";
  case LLVM_IR_IndexAdd :           return "IndexAdd";
  case LLVM_IR_SilentStore :        return "SilentStore";
  case LLVM_IR_Sine :               return "Sine";
  case LLVM_IR_Cosine :             return "Cosine";
  default:                          return std::to_string(microop) + "???";
  }
}
