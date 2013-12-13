using System;
using System.Text;
using System.IO;
using System.Threading;
using System.Linq;
using System.Collections.Generic;
using Mono.Cecil;

public class DotNetClassExtract
{

   public static void Main(string [] args)
   {
      //if (args.Length < 2) {
      //   Console.Error.WriteLine("Please provide directory");
      //   Environment.Exit(-1);
      //}

      //IEnumerable<string> files =  Directory.GetFiles(args[1], "*.dll", SearchOption.AllDirectories);
      IEnumerable<string> files =  Directory.GetFiles("../../../res", "*.dll", SearchOption.AllDirectories);

      foreach (var f in files) {
         var assembly = AssemblyDefinition.ReadAssembly(f);
         var types =
            from module in assembly.Modules.Cast<ModuleDefinition>()
            from type in module.Types.Cast<TypeDefinition>()
            where type.Namespace != null && type.Namespace.StartsWith("System")
            select type;

         foreach (var t in types) {
            foreach(var m in t.Methods.Cast<MethodDefinition>()) {
               Console.WriteLine(
                     new StringBuilder()
                     .Append(t.Namespace)
                     .Append(" ")
                     .Append(t.Name)
                     .Append(" ")
                     .Append(m.FullName)
                     );
            }
         }
      }

   }
}
