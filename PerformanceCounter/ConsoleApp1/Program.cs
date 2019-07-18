using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class Program
    {
        static void Main( )
        {
            PerformanceCounter perfCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");

            PerformanceCounter ramCounter = new PerformanceCounter("Memory", "% Committed Bytes In Use", null);
            PerformanceCounter AvailableMem = new PerformanceCounter("Memory", "Available MBytes", null);

            perfCounter.NextValue();
         

            // Initialize to start capturing


            for (int i = 0; i < 200; i++)
            {
                // give some time to accumulate data
                Thread.Sleep(1000);
             

               

                Console.WriteLine(i + " CPU: " + perfCounter.NextValue()+"  Committed Bytes in use  :"+(ramCounter.NextValue()) + " available mem:"+AvailableMem.NextValue());
            } 
            Console.ReadKey();
        }
    }
}
