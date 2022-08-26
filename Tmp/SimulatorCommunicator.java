package org.iitis.implementation;

import org.iitis.Identificators.Identificator;
import org.iitis.json.JSONArray;
import org.iitis.json.JSONObject;
import org.iitis.unified.ForwardingDevice;
import org.iitis.unified.NetState;
import org.iitis.unified.Node;
import org.iitis.unified.PacketInfo;
import org.iitis.unified.PathFlow;
import org.iitis.unified.PathTranslator;
import org.iitis.unified.PortDeviceIdTuple;
import org.iitis.unified.UnifiedCommunicationModule;

import java.io.File;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.Scanner;

public class SimulatorCommunicator
{
    private String topologyFile;
    private String pipeName;
    private RandomAccessFile pipe;
    private UnifiedCommunicationModule mod;
    public SimulatorCommunicator( String topologyFile, String pipeName)
    {  
		//System.exit(1); // UWAGA PP : tu proces powinien sie zakonczyc
		System.err.println("Zglasza sie SimulatorCommunicator (stderr)");
        System.out.println("Zglasza sie SimulatorCommunicator (stdout)");
        System.out.flush();
        System.err.flush();
        mod = new UnifiedCommunicationModule(new PathInstallerSimulator(),new SimulatorLogger());
        try {
            this.pipeName = pipeName;
            this.topologyFile = topologyFile;
            RandomAccessFile pipe;
            while (true) {
                try {
                    pipe = new RandomAccessFile(pipeName, "rw"); //czekamy co 200 ms na utworzenie pipe przez Server (c++ omnetpp)
                    this.pipe = pipe;
                    break;

                } catch (Exception e) {
                }
                Thread.sleep(100);
            }
        }catch (Exception e){}
    }
    public ArrayList<ForwardingDevice> getTopology()
    {
        ArrayList<ForwardingDevice> topology = new ArrayList<ForwardingDevice>();
        String configJson = "";
        try {
            Scanner scanner = new Scanner(new File(topologyFile));
            configJson = scanner.useDelimiter("\\A").next();
            scanner.close();
        }catch (Exception e)
        {
            System.out.println("ERROR: Topology malfunction");
            return null;
        }
        try
        {

            JSONObject tmp = new JSONObject(configJson);
            JSONArray topologyJson = tmp.getJSONArray("devices");
            for (int i = 0; i <topologyJson.length(); i++)
            {
                JSONObject fdJson = (JSONObject) topologyJson.get(i);
                int simpleID = fdJson.getInt("device id");
                ArrayList<PortDeviceIdTuple> links = new ArrayList<PortDeviceIdTuple>();
                JSONArray linksJson = (JSONArray) fdJson.getJSONArray("links");
                for (int j = 0; j < linksJson.length(); j++)
                {
                    JSONObject linkJson = (JSONObject) linksJson.get(j);
                    PortDeviceIdTuple link = new PortDeviceIdTuple(j, linkJson.getInt("device id"),linkJson.getLong("port number"));
                    links.add(link);
                }
                ArrayList<Identificator> hosts = new ArrayList<>();
                JSONArray hostsJson = (JSONArray) fdJson.getJSONArray("hosts");
                for (int j = 0; j < hostsJson.length(); j++)
                {
                    JSONObject hostJson = (JSONObject) hostsJson.get(j);
                    hosts.add(new HostIdSimulator(hostJson.getLong("id host")));
                }
                ForwardingDevice fd = new ForwardingDevice(links.size(),simpleID, simpleID);
                fd.setConnectedHosts(hosts);
                fd.links = links;
                topology.add(fd);
            }

        }catch (Exception e)
        {
            System.out.println("ERROR: "+e.getMessage());
            return null;
        }
        return topology;
    }

    public boolean getNewPacketInfo()
    {
        String configJson = "";
        try {
            configJson = this.pipe.readLine();
            UnifiedCommunicationModule.log.info(configJson);
        }
        catch (Exception e)
        {
            System.out.println("ERROR: Packet malfunction. Pipe not able to read from");
            return false;
        }
        try {
            JSONObject information = new JSONObject(configJson);
            information = information.getJSONObject("information");
            JSONArray packets = information.getJSONArray("packets");
            for (int i = 0; i <packets.length(); i++)
            {
                JSONObject packet = packets.getJSONObject(i);
                PacketInfo cognitivePacket = new PacketInfo(packet.getString("payload"));
                UnifiedCommunicationModule.receivePacketInfo(cognitivePacket);
            }
        }
        catch (Exception e) {
            System.out.println("ERROR: Problem parsing packet file : "+e.getMessage());
            try {
                pipe.write(e.getMessage().getBytes());
                return false;
            }catch (Exception e1)
            {
                System.out.println("UNABLE TO WRITE CAUSE OF CRASH TO PIPE");
                return false;
            }

        }
        return true;
    }
    public void publishPaths()
    {
        JSONObject paths = new JSONObject();
        JSONArray pathsArray = new JSONArray();
        ArrayList<PathFlow> pathsFlow = PathTranslator.getBestPaths();
        for (int i = 0; i < pathsFlow.size(); i++)
        {
            JSONObject singlePath = new JSONObject();
            JSONArray nodes = new JSONArray();
            ArrayList<Node> nodesFlow = pathsFlow.get(i).getPath();
            for (int j = 0; j < nodesFlow.size(); j++)
            {
                JSONObject node = new JSONObject();
                node.put("device id", nodesFlow.get(j).getNodeDeviceId());
                node.put("output port", nodesFlow.get(j).getOutputPort());
                nodes.put(node);
            }
            singlePath.put("src",pathsFlow.get(i).getSource());
            singlePath.put("dst",pathsFlow.get(i).getDestination());
            singlePath.put("nodes",nodes);
            if(NetState.PATH_FORMAT == NetState.PathFormat.HOST_SPECIFIC)
            {
                singlePath.put("host id dst",pathsFlow.get(i).getDstHostId().toLong());
                singlePath.put("host id src", pathsFlow.get(i).getSrcHostId().toLong());
            }
            pathsArray.put(singlePath);
            UnifiedCommunicationModule.log.info(pathsFlow.get(i).toString());
        }
        paths.put("paths", pathsArray);

        try {
            this.pipe.write(paths.toString().getBytes());
        }
        catch (Exception e){}
    }
    public void roundRobinPackets()
    {
        for (int i = 0; i < NetState.getTopology().size(); i++)
        {
            for (int j = 0; j < NetState.getTopology().size(); j++)
            {

                if(i!=j)
                {
                    PacketInfo mockPacket = new PacketInfo("~"+NetState.getTopology().get(i).getSimpleID()+"~"+0+"~"+NetState.getTopology().get(j).getSimpleID());
                    UnifiedCommunicationModule.receivePacketInfo(mockPacket);
                }
            }
        }
    }

}
