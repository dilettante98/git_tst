using System;
using System.Collections.Generic;
using System.Management;
public class Hi
{
    public static void Main()
    {

        // ConnectionOptions options = new ConnectionOptions();

        // set the options.Username and 
        // options.Password properties to the correct values  
        // options.Authority = "ntlmdomain:DOMAIN";
        // and replace DOMAIN with the remote computer's
        // domain.  You can also use Kerberos instead
        // of ntlmdomain.


        // Make a connection to a remote computer.
        // Replace the "FullComputerName" section of the
        // string "\\\\FullComputerName\\root\\cimv2" with
        // the full computer name or IP address of the
        // remote computer.
        ManagementScope scope = new ManagementScope("\\\\BLRLT510FRQ2\\root\\cimv2");
        scope.Connect();
        List<string> Keys = new List<string> {    "Win32_Processor", " Win32_PhysicalMemory" , "Win32_PerfFormattedData_PerfOS_Processor", "Win32_OperatingSystem" };
       foreach (var Key in Keys)
        {
            Console.WriteLine("----------------");
            ObjectQuery query = new ObjectQuery("SELECT * FROM " + Key);
            {
                ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);
                //  ManagementObjectCollection queryCollection = searcher.Get();

                foreach (ManagementObject share in searcher.Get())
                {
                    int count = 0;
                    foreach (PropertyData PropertyDataCollection in share.Properties)
                    {


                        Console.WriteLine( count+" " + Key + "|" + PropertyDataCollection.Name + " :" + PropertyDataCollection.Value);
                        //if(PropertyDataCollection.Name== "BUILTIN")
                        count++;
                        if (PropertyDataCollection.Value == null)
                            Console.WriteLine("====================");

                    }
                }
            }

            Console.ReadKey();
        }
    }
}