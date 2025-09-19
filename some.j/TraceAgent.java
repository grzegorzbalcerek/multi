
import java.io.*;
import java.lang.instrument.*;
import java.security.*;
import java.text.*;
import java.util.*;
import org.objectweb.asm.*;
import org.objectweb.asm.commons.*;
import org.objectweb.asm.util.*;
import static org.objectweb.asm.Opcodes.*;

class TraceAgentPremain {
  public static void premain(String agentArgs,
                             Instrumentation inst) {
    inst.addTransformer(new TraceAgentTransformer());
  }
}

class TraceAgentTransformer implements ClassFileTransformer {
  public byte[] transform(ClassLoader loader, String className,
                          Class<?> classBeingRedefined,
                          ProtectionDomain protectionDomain,
                          byte[] classfileBuffer) {
    final ClassWriter cw = new ClassWriter(0);
    final ClassAdapter ca = new TraceAgentClassAdapter(
                                             cw, className);
    final ClassReader cr = new ClassReader(classfileBuffer);
    cr.accept(ca, 0);
    return cw.toByteArray();
  }
}

class TraceAgentClassAdapter extends ClassAdapter {
  private String className;
  TraceAgentClassAdapter(ClassVisitor cv, String className) {
    super(cv);
    this.className = className;
  }
  @Override
  public MethodVisitor visitMethod(final int access,
                                   final String name,
                                   final String desc,
                                   final String signature,
                                   final String[] exceptions) {
    final MethodVisitor mv0 = cv.visitMethod(access, name,
                                             desc, signature,
                                             exceptions);
    return new TraceAgentMethodAdapter(mv0, name,
                                       desc, className);
  }
}

class TraceAgentMethodAdapter extends MethodAdapter {
  private String description;
  private String name;
  TraceAgentMethodAdapter(MethodVisitor mv, String name,
                     String desc, String className) {
    super(mv);
    this.description = className + "." + name + desc;
    this.name = name;
  }
  @Override public void visitCode() {
    mv.visitCode();
    if (!name.startsWith("<"))
      addTrace("Entering       : " + description);
  }
  private void addTrace(String msg) {
      mv.visitFieldInsn(GETSTATIC, "java/lang/System",
                "out", "Ljava/io/PrintStream;");
      mv.visitLdcInsn(msg);
      mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream",
                 "println", "(Ljava/lang/String;)V");
  }
  @Override public void visitInsn(int opcode) {
    if (!name.startsWith("<")) {
      if (opcode == ATHROW)
        addTrace("Exception from : " + description);
      else if (opcode == IRETURN || opcode == LRETURN ||
               opcode == FRETURN || opcode == DRETURN ||
               opcode == ARETURN || opcode == RETURN)
        addTrace("Returning from : " + description);
    }
    mv.visitInsn(opcode);
  }
  @Override public void visitMaxs(int maxStack, int maxLocals) {
    mv.visitMaxs(maxStack+2, maxLocals);
  }
}
