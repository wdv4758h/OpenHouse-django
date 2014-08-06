# 資訊組雜記 更新日期:2013.12.09

以下為資訊組雜西雜八的事項紀錄…

# OpenHouse主機

位於就輔組內，為自組個人 PC，主要功能為提供 OH 各項服務，僅資訊組有權限登入。

作業系統已於 *2012-09-22* 重灌為 `Arch Linux x86_64`，bootloader 為`grub2`。

---
## 硬體

- CPU: AMD Athlon(tm) II X4 640 Processor
- RAM: 1794576 KB
- disk: 1TB / 500GB / 1TB

### lsblk

    NAME     MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
    sda        8:0    0 931.5G  0 disk
    └─sda1     8:1    0 931.5G  0 part
      └─md1    9:1    0 931.4G  0 raid1 /mnt/md1
    sdb        8:16   0 465.8G  0 disk
    ├─sdb1     8:17   0   128M  0 part  /boot
    ├─sdb2     8:18   0     4G  0 part  [SWAP]
    ├─sdb3     8:19   0    80G  0 part  /
    ├─sdb4     8:20   0    40G  0 part  /var
    ├─sdb5     8:21   0 341.6G  0 part  /home
    └─sdb128 259:0    0     2M  0 part
    sdc        8:32   0 931.5G  0 disk
    └─sdc1     8:33   0 931.5G  0 part
      └─md1    9:1    0 931.4G  0 raid1 /mnt/md1

### 硬碟使用狀況

- xatier: 這邊的 `sda` 應該是 `sdb`. `sd[bc]` 應該是 `sd[ac]` 請見 `lsblk/df -h` 結果)

#### /dev/sda

為系統專用碟，大小為500GB，分割表為GPT。

<table class="table">
    <thead>
        <tr><th>Partition</th><th>Size</th><th>Filesystem</th><th>Mountpoint</th></tr>
    </thead>
    <tbody>
        <tr><td>/dev/sda1</td><td>128.0 MiB</td><td>ext4</td><td>/boot</td></tr>
        <tr><td>/dev/sda2</td><td>2.0 GiB</td><td>N/A</td><td>swap</td></tr>
        <tr><td>/dev/sda3</td><td>80.0 GiB</td><td>ext4</td><td>/</td></tr>
        <tr><td>/dev/sda4</td><td>40.0 GiB</td><td>reiserfs</td><td>/var</td></tr>
        <tr><td>/dev/sda5</td><td>341.6 GiB</td><td>ext4</td><td>/home</td></tr>
        <tr><td>/dev/sda128</td><td>2.0 MiB</td><td>N/A</td><td>BIOS boot partition (for grub2)</td></tr>
    </tbody>
</table>

#### /dev/sd[bc]

兩顆皆為資料碟，容量皆為1TB，分割表皆為GPT

只有一個分割槽，為對重要資料做備份，兩分割槽使用 `mdadm` 做軟體 RAID 1（mirror），使用新版的1.2 metadata

產生之 device 為 `/dev/md1`，預設 mount 在 `/mnt/md1`，檔案系統為 ext4（有ACL）

資料直接放在 `/mnt/md1` 底下，再用 rebind 的方式 mount 到正確的位置（`/srv/ftp`、`/srv/http`……）

各目錄用途如下：

* **ftp**：     FTP的根目錄，rebind 至 `/srv/ftp`
* **graduate**：舊畢聯會網站備份
* **home**：    舊 `/home` 目錄備份
* **http**：    HTTP 服務的根目錄，rebind 至 `/srv/http`
* **mysql**：   為 MySQL 資料庫的每日備份
* **qemu**：    為舊 debian 系統的虛擬機器的映像檔放置處，rebind 至 `/home/qemu`
* **root**：    舊 debian 系統之 `/` 備份
* **root2**：   測試用 Arch Linux之 `/` 備份
* **www**：     舊 `/home/www` 目錄備份

---

## 網路

使用學校分配的固定IP：

(2013/08/19 OH主機跟著就輔組從行政大樓B1搬到計中三樓，IP 從 `140.113.101.10` 變成  `140.113.99.69`)

    IP        140.113.99.69
    Gateway   140.113.99.94
    Netmask   255.255.255.224
    Hostname  openhouse.nctu.edu.tw

---

## 帳號／權限管理

僅資訊組有 shell 與 sudo（wheel group）權限，除非有特殊需求，嚴禁開 shell 帳號讓外人使用。
root密碼只有資訊組常用的一組，僅可口耳相傳，嚴禁紀錄在如紙本或其他媒體上。
平時系統管理請ssh至主機上使用sudo。
系統上重要帳號紀錄如下：

### system

* **root**：    不必多說
* **ftp**：     vsftpd 與其他人透過FTP登入時的使用者
* **http**：    apache 運行時的使用者
* **mysql**：   MySQL 運行時的使用者
* **qemu**：    QEMU 虛擬機運行時的使用者
* **postfix**： Postfix MTA 運行時的使用者

### users

* **pkmx**：    2012年資訊組組長
* **m157q**：   2012年資訊組組員、2013年資訊組組長
* **xatier**：  2013年資訊組組員
* **wdv4758h**：2013年資訊組組員

`TODO：將過去資訊組之帳號匯入`

---

## Debian VM & BBS

由於升級至 Arch Linux 時，發現 Maple BBS 與新系統不相容，故仍在 VM 內運行舊debian系統，僅提供 BBS 服務。
虛擬機為qemu，只有分配一顆 40G 硬碟在 `/home/qemu` 下。

+ 2013.12.09

重寫了一份 /etc/systemd/system/qemu@bbs.service
讓系統重開機的時候自動開啟 QEMU 和裡頭的 Debian VM。
因為直接把指令寫在 ExecStart 不會 work，只好寫了 /etc/qemu/script.sh 讓 qemu@bbs 去讀它。

+ 新看板 & 分類

(A)nnounce -> 9 (教學) 站長功能 有說明

### 手動開啟

基本上因為上面的 qemu@bbs 設定好了，所以重開機應該就會自動啟動BBS，如果沒有的話再使用這個 section 紀錄的方法來手動開啟，並記得檢查為何 qemu@bbs 沒有成功跑起來的原因。

---

先確定 kvm 的 kernel module 有 load 進來

    # lsmod | grep kvm

如果確定 kvm kernel module 還沒 load 的話就

    # modprobe kvm

然後再下以下指令開啓qemu

    # qemu-system-x86_64 -runas qemu -vnc :0,password -monitor telnet:127.0.0.1:50652,server,nowait -net nic,model=rtl8139 -net user,hostfwd=tcp::23-:23,hostfwd=tcp::2222-:22 -hda /home/qemu/debian.img >& /dev/null &

目前僅開放兩個服務：

* bbs (telnet)：23（guest）→23（host）
* ssh：22（guest）→2222（host）

### QEMU Monitor
QEMU 提供monitor 界面在文字界面下管理 VM，目前聽在 localhost 的 50652 port：

    $ telnet localhost 50652
    Trying ::1...
    Connection failed: Connection refused
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    QEMU 1.2.0 monitor - type 'help' for more information
    (qemu)
可輸入 help 看指令，如要離開 monitor 請先 escape 至 telnet 的 prompt 再輸入 quit ，**直接在monitor下quit會關掉虛擬機**！

    (qemu) <Hit Ctrl+]>
    telnet> quit
    $
### VNC Console
如有需要進入 VM 之 console，可進入 monitor 後使用 `set_password` 修改密碼：

    (qemu) set_password vnc <password>

預設VNC聽在:0（5900），可用 `vncviewer` 連入：

    $ vncviewer openhouse.nctu.edu.tw:0
    Connected to RFB server, using protocol version 3.8
    Performing standard VNC authentication
    Password:
    Authentication successful
    Desktop name "QEMU"
    VNC server default format:
      32 bits per pixel.
      Least significant byte first in each pixel.
      True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0
    Using default colormap which is TrueColor.  Pixel format:
      32 bits per pixel.
      Least significant byte first in each pixel.
      True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0

---
## 系統維護
請熟讀 Arch Linux 系統管理的基本知識，例如 [pacman](https://wiki.archlinux.org/index.php/Pacman) 、 [AUR](https://wiki.archlinux.org/index.php/Arch_User_Repository) ……等。

### 系統更新
由於 Arch Linux 為 rolling release，需不斷升級保持系統在最新的狀態。大致上更新步驟如下：

* 更新前請注意[Arch Linux官網](http://www.archlinux.org)上之公告，最好也訂閱[arch-dev-public](https://mailman.archlinux.org/mailman/listinfo/arch-dev-public)。
* `sudo pacman -Syu`
* 注意升級過程中是否有任何訊息，亦可查看 `/var/log/pacman.log` ，如有的話，請按照指示進行。
* 由於 `/etc` 下的設定檔可能有所更新，預設 `pacman` 會將新的設定檔加上 `.pacnew` 的suffix，請 `find /etc | grep pacnew` 找出所有`.pacnew`的新設定檔。
* 用 `vimdiff /etc/<filename>{,.pacnew}` 等 diff 程式 merge 新舊的差異，請依照情況修改，不懂就 google。
* 讓各服務 reload 設定檔（如果有改到的話），測試是否有問題。
* 確認一切正常後，可刪除舊有已不需要的檔案（如 `.pacnew` ）。

### logwatch
目前系統上有裝 `logwatch` ，每天凌晨時會寄信給 `root@openhouse.nctu.edu.tw` 整理昨日各log的報表，請檢查是否有問題。

---
## 畢聯會
### ftp/http 共用
畢聯會的主機從去年(102級)和 OH 共用，主要功能就只有宣傳用的靜態網站，沒有後端資料要處理。
網站的目錄在 `/srv/http/graunion/`而因為 `/mnt/md1/ftp/graunion/www/` 用了 `fstab` rebind 到 `/srv/http/graunion/` (請看 `/etc/fstab`)

所以畢聯會直接從 ftp 上傳網頁檔案到 `/srv/ftp/graunion/www/` 後就可以直接用網頁瀏覽器連 `graunion.nctu.edu.tw`  看到網頁，因為 `/srv/ftp/graunion/www/` 和 `/srv/http/graunion/` 其實是一樣的，請進去看了就知道了

    2014OH(2013Fall~) 畢聯會改用 weebly 架站，直接把畢聯會的domain導到 weebly 做出來的網站了，所以沒有用到ftp的功能。

## Virtual Host
OH 的 `apache` 有設定畢聯會的 Virtual Host
設定檔在 `/etc/httpd/conf/extra/httpd-vhosts.conf`
連到 `http://graunion.nctu.edu.tw` 會導到 `/srv/http/graunion/`
如果連 `http://openhouse.nctu.edu.tw/graunion/` 也會被導到 `http://graunion.nctu.edu.tw`
其餘詳細請看 virtual host 設定檔

---
## LAMP

---
## FTP

+ 使用 vsftpd
+ /srv/ftp/年份/組別
    + 新資料夾
        + mkdir /srv/ftp/2015/
        + chown root:ftp /srv/ftp/2015/ && chmod 775 /srv/ftp/2015/
        + chown root:root /srv/ftp/2014/ && chmod 755 /srv/ftp/2014/
        + 建立子資料夾 (依組分)
+ 每年更新帳號，boss一組，組員們一組，基本上帳號就是當屆使用而已，不留歷屆帳號。
+ 設定檔在 /etc/vsftpd.conf 和 /etc/vsftpd/
    + /etc/vsftpd/logins.txt
        + 可以設定帳號和密碼
        + 設定完之後記得執行 /etc/vsftpd/rebuild_logins.sh 讓 vsftpd 的帳號密碼資料庫更新
    + /etc/vsftpd/users/
        + 根據帳號設定根目錄
            + 檔名：帳號
            + 內容：登入後的根目錄位置
        + sed -i 's/2014/2015/g' /etc/vsftpd/users/oh2014 && mv /etc/vsftpd/users/oh2014 /etc/vsftpd/users/oh2015

---
## Postfix MTA

+ 每年要更新 `/etc/postfix/aliases`
    + root 改為當年度的 infoxx 群組
    + oh20xx 群組加入廣廣跟當年度的組長群 email
    + 改完 `/etc/postfix/aliases` 後，記得下 `sudo postalias /etc/postfix/aliases` 更新 aliases.db
