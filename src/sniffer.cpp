#include <iostream>
#include <atomic>
#include <tins/tins.h>

using namespace Tins;

struct CaptureStats {
    std::atomic<int> totalPackets{0};
};

static Sniffer* g_sniffer = nullptr;

static bool onPacketArrives(PDU& pdu, CaptureStats* stats) {
    int count = ++stats->totalPackets;

    const Dot11* dot11 = pdu.find_pdu<Dot11>();
     if (dot11 == nullptr) {                 
        std::cout << "[+] Packet #" << count << ", size: " << pdu.size() << " bytes\n";
        return true;                                                   
    }

    if (const Dot11Beacon* beacon = pdu.find_pdu<Dot11Beacon>()) {
        std::cout << "[Beacon-frame] #" << count << " | SSID: " << beacon->ssid() << " | BSSID: " << beacon->addr2() << "\n";
    }
    else if (const Dot11ProbeRequest* probeReq = pdu.find_pdu<Dot11ProbeRequest>()) {
        std::cout << "[Probe Request] #" << count << " | SSID: " << probeReq->ssid() << " | BSSID: " << probeReq->addr2() << " -> " << probeReq->addr1() <<  "\n";
    }
    else if (const Dot11ProbeResponse* probeResp = pdu.find_pdu<Dot11ProbeResponse>()) {
        std::cout << "[Probe Response] #" << count << " | SSID: " << probeResp->ssid() << " | BSSID: " << probeResp->addr2() << " -> "  << probeResp->addr1() <<  "\n";
    }
    else if (const Dot11AssocRequest* assocReq = pdu.find_pdu<Dot11AssocRequest>()) {
        std::cout << "[Association Request] #" << count << " | BSSID: " << assocReq->addr2() << " -> " << assocReq->addr1() << "\n";
    }
    else if (const Dot11ReAssocRequest* reassocReq = pdu.find_pdu<Dot11ReAssocRequest>()) {
        std::cout << "[ReAssociation Request] #" << count << " | BSSID: " << reassocReq->addr2() << " -> " << reassocReq->addr1() << "\n";
    }
    else if (const Dot11AssocResponse* assocResp = pdu.find_pdu<Dot11AssocResponse>()) {
        std::cout << "[Association Response] #" << count << " | BSSID: " << assocResp->addr2() << " -> " << assocResp->addr1() <<"\n";
    }
    else if (const Dot11ReAssocResponse* reassocResp = pdu.find_pdu<Dot11ReAssocResponse>()) {
        std::cout << "[ReAssociation Response] #" << count << " | BSSID: " << reassocResp->addr2() << " -> " << reassocResp->addr1() << "\n";
    }
    else if (const Dot11Disassoc* disassoc = pdu.find_pdu<Dot11Disassoc>()) {
        std::cout << "[Disassociation-frame] #" << count << " | BSSID: " << disassoc->addr2() << " -> " << disassoc->addr1() << "\n";
    }

    else if (const Dot11Authentication* auth = pdu.find_pdu<Dot11Authentication>()) {
        std::cout << "[Authentication-frame] #" << count << " | BSSID: " << auth->addr2() << " -> " << auth->addr1() <<"\n";
    }
    else if (const Dot11Deauthentication* deauth = pdu.find_pdu<Dot11Deauthentication>()) {
        std::cout << "[Deauthentication-frame] #" << count << " | BSSID: " << deauth->addr2() << " -> " << deauth->addr1() << "\n";
    }
    else if(const Dot11Ack* ACK = pdu.find_pdu<Dot11Ack>()){
        std::cout << "[ACK] #" << count << " | to: " << ACK->addr1() << "\n";
    }
    else if (const Dot11RTS* rts = pdu.find_pdu<Dot11RTS>()) {
        std::cout << "[RTS] #" << count << " | to: " << rts->target_addr() << "\n";
    }
    else if (dot11->type() == Dot11::CONTROL && dot11->subtype() == Dot11::CTS) {  
        std::cout << "[CTS] #" << count << " | to: " << dot11->addr1() << "\n";
    }
    else if (const Dot11PSPoll* ps_poll = pdu.find_pdu<Dot11PSPoll>()) {
        std::cout << "[PS_POLL] #" << count << " | to: " << ps_poll->addr1() << "\n";
    }
    else if (const Dot11BlockAck* blockack = pdu.find_pdu<Dot11BlockAck>()) {
        std::cout << "[Block Ack] #" << count << " | to: " << blockack->addr1() <<"\n";
    }
    else if (const Dot11BlockAckRequest* blockackrequest = pdu.find_pdu<Dot11BlockAckRequest>()) {
        std::cout << "[Block Ack Request] #" << count << " | to: " << blockackrequest->addr1() <<"\n";
    }


    else if (const Dot11Data* dataFrame = pdu.find_pdu<Dot11Data>()) {
        if (pdu.find_pdu<RSNEAPOL>() != nullptr) {
            std::cout << "[EAPOL / 4-Way Handshake] #" << count << " | BSSID: " << dataFrame->addr2() << " -> " << dataFrame->addr1() <<"\n";
        }
        else if (pdu.find_pdu<DHCP>() != nullptr) {
            std::cout << "[DHCP] #" << count << "\n";
        }
        else {
            std::cout << "[Data-frame] #" << count << " | size: " << pdu.size() << " bytes\n";
        }
    }
    else {
        std::cout << "[Other] #" << count
                   << " type: " << static_cast<int>(dot11->type()) << "\n";
    }


    return true;
}

extern "C" {

int sniffing(const char* interface, int* outTotalPackets) {
    std::cout << "Target interface: " << interface << std::endl;

    try {
        SnifferConfiguration config;
        config.set_promisc_mode(true);

        Sniffer sniffer(interface, config);
        g_sniffer = &sniffer;

        CaptureStats stats;

        sniffer.sniff_loop([&stats](PDU& pdu) {
            return onPacketArrives(pdu, &stats);
        });

        g_sniffer = nullptr;

        if (outTotalPackets != nullptr) {
            *outTotalPackets = stats.totalPackets.load();
        }

        return 0;
    } catch (const std::exception& e) {
    std::string errorMsg = e.what();

    if (errorMsg.find("CAP_NET_RAW") != std::string::npos) {
        std::cerr << "AirSwitcher needs root permissions to work. "
                     "Launch the script as root user or using 'sudo'\n";
    } else {
        std::cerr << "[-] Error: " << e.what() << "\n";
    }

    g_sniffer = nullptr;
    return -1;
}
}

void stop_capture() {
    if (g_sniffer != nullptr) {
        g_sniffer->stop_sniff();
    }
}

} 