
import java.io.*;
import java.lang.instrument.*;
import java.security.*;
import java.text.*;
import java.util.*;
import org.objectweb.asm.*;
import org.objectweb.asm.commons.*;
import org.objectweb.asm.util.*;
import static org.objectweb.asm.Opcodes.*;

public class TraceAgent implements ClassFileTransformer {
    public static void premain(String agentArgs, Instrumentation inst) {
        inst.addTransformer(new MethodTraceAgent());
    }
    public byte[] transform(ClassLoader loader, final String className, Class<?> classBeingRedefined,
                     ProtectionDomain protectionDomain, byte[] classfileBuffer) {
        final ClassReader cr = new ClassReader(classfileBuffer);
        final ClassWriter cw = new ClassWriter(0);
        final ClassAdapter ca = new ClassAdapter(cw) {
            };
        cr.accept(ca, 0);
        return cw.toByteArray();
    }
}

class TraceClassAdapter extends ClassAdapter {
    TraceClassAdapter(ClassVisitor cv) { super(cv); }
    @Override public MethodVisitor visitMethod(final int access, final String name,
                                               final String desc, final String signature,
                                               final String[] exceptions) {
        final MethodVisitor mv0 = cv.visitMethod(access, name, desc, signature, exceptions);
        return new MethodTraceAdder(mv0, name, desc, className);
    }
}

class MethodTraceAdder extends MethodAdapter {
    private String description;
    private String name;
    MethodTraceAdder(MethodVisitor mv, String name, String desc, String className) {
        super(mv);
        this.description = className + "." + name + desc;
        this.name = name;
    }
    public void visitCode() {
        mv.visitCode();
        if (!name.startsWith("<")) addTrace("Entering       : " + description);
    }
    public void visitInsn(int opcode) {
        if (!name.startsWith("<")) {
            if (opcode == ATHROW)
                addTrace("Exception from : " + description);
            else if (opcode == IRETURN || opcode == LRETURN || opcode == FRETURN ||
                     opcode == DRETURN || opcode == ARETURN || opcode == RETURN)
                addTrace("Returning from : " + description);
        }
        mv.visitInsn(opcode);
    }
    public void visitMaxs(int maxStack, int maxLocals) {
        mv.visitMaxs(maxStack+2, maxLocals);
    }
    private void addTrace(String msg) {
            mv.visitFieldInsn(GETSTATIC, "java/lang/System",
                              "out", "Ljava/io/PrintStream;");
            mv.visitLdcInsn(msg);
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream",
                               "println", "(Ljava/lang/String;)V");

    }
}
