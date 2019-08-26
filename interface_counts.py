
import re
import sys
import os.path

def physical_interface_traffic_statistics(output_file):
    pits = {}
    for _ in range(4):
        line_key_val = output_file.readline().strip().split(':')
        pits[line_key_val[0].strip()] = line_key_val[1].strip()
    return pits

def IPv6_transit_statistics(output_file):
    ipv6ts = {}
    for _ in range(4):
        line_key_val = output_file.readline().strip().split(':')
        ipv6ts[line_key_val[0].strip()] = line_key_val[1].strip()
    return ipv6ts

def Dropped_traffic_statistics_due_to_STP_state(output_file):
    stpdropts = {}
    for _ in range(4):
        line_key_val = output_file.readline().strip().split(':')
        stpdropts[line_key_val[0].strip()] = line_key_val[1].strip()
    return stpdropts

def input_errors(output_file):
    input_errors = {}
    errors = output_file.readline().strip().split(",")
    for error in errors:
        key_val=error.split(":")
        input_errors[key_val[0].strip()] = key_val[1].strip()
    return  input_errors

def output_errors(output_file):
    output_errors = {}
    errors = output_file.readline().strip().split(",")
    for error in errors:
        key_val = error.split(":")
        output_errors[key_val[0].strip()] = key_val[1].strip()
    return output_errors

def PCS_error(output_file):
    pcs = {}
    for _ in range(2):
        pcs_errors = re.split(r'\s+', output_file.readline().strip())
        pcs[pcs_errors[0].strip()] = pcs_errors[1].strip()
    return pcs

def FEC_errors(output_file):
    fec = {}
    for _ in range(4):
        fec_error = re.split(r'\s+', output_file.readline().strip())
        fec[fec_error[0].strip()] = fec_error[1].strip()
    return fec

def MAC_statistics(output_file):
    mac = {}
    receive = {}
    transmit = {}
    for _ in range(15):
        mac_stat = re.split(r'\s\s+', output_file.readline().strip())
        if len(mac_stat) == 3:
            receive[mac_stat[0].strip()] = mac_stat[1].strip()
            transmit[mac_stat[0].strip()] = mac_stat[2].strip()
        if len(mac_stat) == 2:
            receive[mac_stat[0].strip()] = mac_stat[1].strip()
    mac["receive"] = receive
    mac["transmit"] = transmit
    return mac

def filter_statistics(output_file):
    filter = {}
    for _ in range(7):
        filter_line = re.split(r'\s\s+', output_file.readline().strip())
        filter[filter_line[0].strip()] = filter_line[1].strip()
    for cam in output_file.readline().strip().split(','):
        filter[cam.split(":")[0].strip()] = cam.split(":")[1].strip()
    return filter

def logical_interface_1st_traffic_statistics(output_file):
    return IPv6_transit_statistics(output_file)

def logical_interface_local_statistics(output_file):
    return IPv6_transit_statistics(output_file)

def logical_interface_transit_statistics(output_file):
    return physical_interface_traffic_statistics(output_file)

if __name__ == "__main__":
    if sys.argv[1]:
        if os.path.isfile(sys.argv[1]):
            with open(sys.argv[1], 'r') as file:
                line = file.readline()
                interface = {}
                physical_interface_name = ['fe','ge','xe','et']
                while line:
                    if "Physical interface" in line:
                        interface_name = line.split(',')[0].split(':')[1].strip()
                        if interface_name.split('-')[0] in physical_interface_name:
                            interface[interface_name] = {}
                            line = file.readline()
                            while line:
                                if "Traffic statistics:" in line:
                                    interface[interface_name]["Traffic statistics"] = physical_interface_traffic_statistics(file)
                                if "IPv6 transit statistics:" in line:
                                    interface[interface_name]["IPv6 transit statistics"] = IPv6_transit_statistics(file)
                                if "Dropped traffic statistics due to STP State:" in line:
                                    interface[interface_name]["Dropped traffic statistics due to STP State"] = Dropped_traffic_statistics_due_to_STP_state(file)
                                if "Input errors:" in line:
                                    interface[interface_name]["Input errors"] = input_errors(file)
                                if "Output errors:" in line:
                                    interface[interface_name]["output error"] = output_errors(file)
                                if "PCS statistics" in line:
                                    interface[interface_name]["PCS statistics"] = PCS_error(file)
                                if "Ethernet FEC statistics" in line:
                                    interface[interface_name]["Ethernet FEC statistics"] = FEC_errors(file)
                                if "MAC statistics:" in line:
                                    interface[interface_name]["MAC statistics"] = MAC_statistics(file)
                                if "Filter statistics:" in line:
                                    interface[interface_name]['Filter statistics'] = filter_statistics(file)
                                if not line.strip():
                                    print("The physical interface ", interface_name, " counter has proceeded","Move on to next interface!")
                                    break
                                line = file.readline()
                    if "Logical interface" in line:
                        interface_name = line.strip().split(" ")[2]
                        if interface_name.split('-')[0] in physical_interface_name:
                            interface[interface_name] = {}
                            line = file.readline()
                            while line:
                                if "Traffic statistics:" in line:
                                    interface[interface_name]["logical interface Traffic statistics"] = logical_interface_1st_traffic_statistics(file)
                                if "Local statistics:" in line:
                                    interface[interface_name]["logical interface local statistics"] = logical_interface_local_statistics(file)
                                if "Transit statistics:" in line:
                                    interface[interface_name]["logical interface transit statistics"] = logical_interface_transit_statistics(file)
                                if not line.strip():
                                    print("The logical interface ", interface_name, " counter has proceeded","Move on to next intreface!")
                                    break
                                line = file.readline()
                    line = file.readline()

