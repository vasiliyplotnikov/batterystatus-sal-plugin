# mac_battery_health.rb
Facter.add(:mac_battery_health) do
  confine kernel: 'Darwin', mac_laptop: true
  setcode do
    output = Facter::Util::Resolution.exec("/usr/sbin/ioreg -r -c 'AppleSmartBattery'")

    if output.nil? || output.empty?
      false
    else

      batt_status = output.lines.select { |line| line =~ /PermanentFailureStatus/ }[0].split(' ')[2]

      if batt_status == '0'
        true
      else
        false
      end
    end
  end
end
