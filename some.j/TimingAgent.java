
import java.io.*;
import java.lang.instrument.*;
import java.security.*;
import java.text.*;
import java.util.*;
import org.objectweb.asm.*;
import org.objectweb.asm.commons.*;
import org.objectweb.asm.util.*;
import static org.objectweb.asm.Opcodes.*;

public class MethodTraceAgent implements ClassFileTransformer {
    public static void premain(String agentArgs, Instrumentation inst) {
        inst.addTransformer(new Agent());
    }
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
                     ProtectionDomain protectionDomain, byte[] classfileBuffer) {
        final ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
        final TraceClassVisitor tcv = new TraceClassVisitor(cw, new PrintWriter(System.out));
        final ClassAdapter ca = new ClassAdapter(tcv) {
                @Override public MethodVisitor visitMethod(final int access, final String name,
                                                           final String desc, final String signature,
                                                           final String[] exceptions) {
                    final MethodVisitor mv0 = cv.visitMethod(access, name, desc, signature, exceptions);
                    return new MethodTraceAdder(mv0, access, name, desc);
                }
            };
        final ClassReader cr = new ClassReader(classfileBuffer);
        cr.accept(ca, 0);
        return cw.toByteArray();
    }
}

class MethodTraceAdder extends AdviceAdapter {
    private String description;
    MethodEntryExitMsgAdder(MethodVisitor mv, int access, String name, String desc) {
        super(mv, access, name, desc);
        this.description = name + desc;
    }
    public void onMethodEnter() {
        mv.visitCode();
        mv.visitFieldInsn(GETSTATIC, "java/lang/System",
                          "out", "Ljava/io/PrintStream;");
        mv.visitLdcInsn("Entering: " + description);
        mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream",
                           "println", "(Ljava/lang/String;)V");
    }
    public void onMethodExit(int opcode) {
        mv.visitFieldInsn(GETSTATIC, "java/lang/System",
                          "out", "Ljava/io/PrintStream;");
        mv.visitLdcInsn("Exiting: " + description);
        mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream",
                           "println", "(Ljava/lang/String;)V");
    }
}
