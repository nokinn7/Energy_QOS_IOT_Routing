#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "ns3/aodv-module.h"
#include "ns3/applications-module.h"
#include "ns3/energy-module.h"
#include <fstream>

using namespace ns3;
using namespace ns3::energy;

NS_LOG_COMPONENT_DEFINE("IoTNetworkSim");

// Function to log remaining energy levels periodically to CSV
void LogEnergy(Ptr<BasicEnergySource> energySource, uint32_t nodeId, std::ofstream *csvFile)
{
    double remainingEnergy = energySource->GetRemainingEnergy();
    double time = Simulator::Now().GetSeconds();
    *csvFile << time << "," << nodeId << "," << remainingEnergy << "\n";
    
    // Schedule next log in 2 seconds
    Simulator::Schedule(Seconds(2.0), &LogEnergy, energySource, nodeId, csvFile);
}

int main(int argc, char *argv[])
{
    uint32_t numNodes = 20;
    double simTime = 30.0; // 30 seconds simulation

    CommandLine cmd(__FILE__);
    cmd.Parse(argc, argv);

    // 1. Create 20 IoT Sensor Nodes and 1 Gateway Node
    NodeContainer sensorNodes;
    sensorNodes.Create(numNodes);
    NodeContainer gatewayNode;
    gatewayNode.Create(1);

    NodeContainer allNodes;
    allNodes.Add(sensorNodes);
    allNodes.Add(gatewayNode);

    // 2. Set Up Spatial Mobility (5x4 Grid Layout)
    MobilityHelper mobility;
    mobility.SetPositionAllocator("ns3::GridPositionAllocator",
                                  "MinX", DoubleValue(0.0),
                                  "MinY", DoubleValue(0.0),
                                  "DeltaX", DoubleValue(15.0),
                                  "DeltaY", DoubleValue(15.0),
                                  "GridWidth", UintegerValue(5),
                                  "LayoutType", StringValue("RowFirst"));
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(allNodes);

    // 3. Configure Wireless Ad-hoc Channel (Wi-Fi 802.11b)
    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211b);

    YansWifiPhyHelper wifiPhy;
    YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default();
    wifiPhy.SetChannel(wifiChannel.Create());

    WifiMacHelper wifiMac;
    wifiMac.SetType("ns3::AdhocWifiMac");

    NetDeviceContainer devices = wifi.Install(wifiPhy, wifiMac, allNodes);

    // 4. Configure Baseline Routing Protocol (AODV)
    AodvHelper aodv;
    InternetStackHelper stack;
    stack.SetRoutingHelper(aodv);
    stack.Install(allNodes);

    // 5. Assign IP Addresses
    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = address.Assign(devices);

    // 6. Attach Energy Models (Installed on all nodes)
    BasicEnergySourceHelper basicSourceHelper;
    basicSourceHelper.Set("BasicEnergySourceInitialEnergyJ", DoubleValue(100.0));
    EnergySourceContainer sources = basicSourceHelper.Install(allNodes);

    WifiRadioEnergyModelHelper radioEnergyHelper;
    radioEnergyHelper.Install(devices, sources);

    // Create CSV logger for energy metrics
    std::ofstream energyLog("energy_logs.csv");
    energyLog << "Time,NodeID,RemainingEnergy\n";

    for (uint32_t i = 0; i < allNodes.GetN(); ++i)
    {
        Ptr<BasicEnergySource> basicSource = DynamicCast<BasicEnergySource>(sources.Get(i));
        Simulator::Schedule(Seconds(1.0), &LogEnergy, basicSource, i, &energyLog);
    }

    // 7. Configure Traffic Flow (Sensors send data packets to Gateway)
    uint16_t port = 9;
    UdpServerHelper server(port);
    ApplicationContainer serverApp = server.Install(gatewayNode.Get(0));
    serverApp.Start(Seconds(1.0));
    serverApp.Stop(Seconds(simTime));

    UdpClientHelper client(interfaces.GetAddress(numNodes), port);
    client.SetAttribute("MaxPackets", UintegerValue(100));
    client.SetAttribute("Interval", TimeValue(Seconds(1.0)));
    client.SetAttribute("PacketSize", UintegerValue(512));

    for (uint32_t i = 0; i < sensorNodes.GetN(); ++i)
    {
        ApplicationContainer clientApp = client.Install(sensorNodes.Get(i));
        clientApp.Start(Seconds(2.0 + (i * 0.1)));
        clientApp.Stop(Seconds(simTime));
    }

    // 8. Output Trace Files for QoS Analysis
    AsciiTraceHelper ascii;
    wifiPhy.EnableAsciiAll(ascii.CreateFileStream("iot_routing_trace.tr"));

    std::cout << "Starting IoT Network Simulation..." << std::endl;
    Simulator::Stop(Seconds(simTime));
    Simulator::Run();
    Simulator::Destroy();
    std::cout << "Simulation Completed Successfully! Output logs generated." << std::endl;

    energyLog.close();
    return 0;
}
