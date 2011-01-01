Summary:	Maildrop mail filter/mail delivery agent
Name:		maildrop
Version:	1.7.0
Release:	%mkrel 23
License:	GPL
Group:		System/Servers
URL:		http://www.flounder.net/~mrsam/maildrop/
Source0:	%{name}-%{version}.tar.bz2
# S1, S2 & P0 originates from:
# http://www.firstpr.com.au/web-mail/Maildrop-mods-filtering/
Source1:	subjadd.c
Source2:	my.mailfilter.txt.bz2
Source3:	README.DELTAG.html.bz2
Patch0:		maildrop-1.5.3-DELTAG.patch
Patch1:		maildrop-1.7.0-0x0B-fix.patch
Patch2:		maildrop-1.7.0-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		maildrop-1.7.0-CVE-2010-0301.diff
BuildRequires:	gdbm-devel
BuildRequires:	openldap-devel
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	libsasl-devel
BuildRequires:	pam-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Maildrop is a combination mail filter/mail delivery agent.
Maildrop reads the message to be delivered to your mailbox,
optionally reads instructions from a file how filter incoming
mail, then based on these instructions may deliver mail to an
alternate mailbox, or forward it, instead of dropping the
message into your mailbox.

Maildrop uses a structured, real, meta-programming language in
order to define filtering instructions.  Its basic features are
fast and efficient.  At sites which carry a light load, the
more advanced, CPU-demanding, features can be used to build
very sophisticated mail filters.  Maildrop deployments have
been reported at sites that support as many as 30,000
mailboxes.

Maildrop mailing list:
http://lists.sourceforge.net/lists/listinfo/courier-maildrop

This version is compiled with support for GDBM database files,
maildir enhancements (folders+quotas), and userdb.

%package	mysql
Summary:	Maildrop mail filter/mail delivery agent with MySQL support
Group:		System/Servers
Requires:	%{name} = %{version}

%description	mysql
Maildrop mail filter/mail delivery agent with MySQL support

%package	openldap
Summary:	Maildrop mail filter/mail delivery agent with OpenLDAP support
Group:		System/Servers
Requires:	%{name} = %{version}

%description	openldap
Maildrop mail filter/mail delivery agent with OpenLDAP support

%package	devel
Summary:	Development tools for handling E-mail messages
Group:		Development/C

%description	devel
The maildrop-devel package contains the libraries and header files
that can be useful in developing software that works with or processes
E-mail messages.

Install the maildrop-devel package if you want to develop applications
which use or process E-mail messages.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1 -b .DELTAG
%patch1 -p1 -b .maildropmysql.cf
%patch2 -p0
%patch3 -p0 -b .CVE-2010-0301

cp %{SOURCE1} subjadd.c
bzcat %{SOURCE2} > my.mailfilter.txt
bzcat %{SOURCE3} > README.DELTAG.html
mv 0README.txt README.DELTAG

%build
export DEFAULT_DEF="./Maildir"
export MAILBOT="%{_bindir}/mailbot"
export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

STD_CONFIGURE="--with-devel --with-etcdir=%{_sysconfdir}/maildrop --enable-userdb \
    --with-db=gdbm --enable-maildirquota --with-trashquota \
    --enable-restrict-trusted=0 --enable-maildrop-uid=root --enable-maildrop-gid=mail \
    --enable-sendmail=%{_sbindir}/sendmail --enable-tempdir=.tmp --enable-smallmsg=8192 \
    --enable-global-timeout=300 --enable-keep-fromline=1 --enable-syslog=1 --with-dirsync"

# configure and make the standard maildrop
%configure2_5x $STD_CONFIGURE \
    --enable-trusted-users="root mail daemon postfix postmaster uucp qmaild sendmail mmdf vpopmail"
perl -pi -e "s|^#define MAILBOT.*|#define MAILBOT \"%{_bindir}/mailbot\"|g" maildrop/mailbot.h
perl -pi -e "s|^#define DEFAULT_DEF.*|#define DEFAULT_DEF \"./Maildir\"|g" maildrop/mailbot.h maildrop/config.h
%make
cp maildrop/maildrop maildrop-STD

pushd maildrop
# configure and make the MySQL aware maildrop
make clean
%configure2_5x \
    --enable-maildropmysql \
    --with-mysqlconfig=%{_sysconfdir}/maildrop/maildrop-mysql.config \
    --enable-trusted-users="root mail daemon postfix postmaster uucp qmaild sendmail mmdf vpopmail mysql" \
    $STD_CONFIGURE
perl -pi -e "s|^#define MAILBOT.*|#define MAILBOT \"%{_bindir}/mailbot\"|g" mailbot.h
perl -pi -e "s|^#define DEFAULT_DEF.*|#define DEFAULT_DEF \"./Maildir\"|g" mailbot.h config.h
%make
cp maildrop ../maildrop-mysql

# configure and make the OpenLDAP aware maildrop
make clean
%configure2_5x \
    --enable-maildropldap \
    --with-ldapconfig=%{_sysconfdir}/maildrop/maildrop-openldap.config \
    --enable-trusted-users="root mail daemon postfix postmaster uucp qmaild sendmail mmdf vpopmail ldap" \
    $STD_CONFIGURE
%make
perl -pi -e "s|^#define DEFAULT_DEF.*|#define DEFAULT_DEF \"./Maildir\"|g" config.h
cp maildrop ../maildrop-openldap

popd

# make the addon
gcc %{optflags} -o subjadd subjadd.c

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_sysconfdir}/maildrop/maildroprcs

# install the extras
install -m755 subjadd %{buildroot}%{_bindir}/
install -m755 maildrop-STD %{buildroot}%{_bindir}/maildrop

install -m755 maildrop-mysql %{buildroot}%{_bindir}/maildrop-mysql
install -m755 maildrop-openldap %{buildroot}%{_bindir}/maildrop-openldap
install -m600 maildropmysql.config %{buildroot}%{_sysconfdir}/maildrop/maildrop-mysql.config
install -m600 maildropldap.config %{buildroot}%{_sysconfdir}/maildrop/maildrop-openldap.config

install -m644 maildir/quotawarnmsg %{buildroot}%{_sysconfdir}/maildrop/quotawarnmsg


cat > %{buildroot}%{_sysconfdir}/maildrop/autoresponsesquota <<EOF
#100000000S,10000C
EOF

cat > %{buildroot}%{_sysconfdir}/maildrop/maildirfilterconfig <<EOF
MAILDIRFILTER=../.mailfilter 
MAILDIR=./Maildir 
EOF

cat > %{buildroot}%{_sysconfdir}/maildrop/maildirshared <<EOF
#
EOF

cat > %{buildroot}%{_sysconfdir}/maildrop/maildroprc <<EOF
#logfile "/var/log/maildrop.log"
EOF

# fix html docs for proper docs inclusion
mv %{buildroot}%{_datadir}/maildrop/html html

# fix: arch-dependent-file-in-usr-share
rm -f %{buildroot}%{_bindir}/userdbpw
mv %{buildroot}%{_datadir}/maildrop/scripts/userdbpw %{buildroot}%{_bindir}/userdbpw

# fix so that these won't conflict with the courier-imap package
mv %{buildroot}%{_bindir}/deliverquota %{buildroot}%{_bindir}/deliverquota-maildrop
mv %{buildroot}%{_bindir}/maildirmake %{buildroot}%{_bindir}/maildirmake-maildrop
mv %{buildroot}%{_bindir}/makeuserdb %{buildroot}%{_bindir}/makeuserdb-maildrop
mv %{buildroot}%{_bindir}/pw2userdb %{buildroot}%{_bindir}/pw2userdb-maildrop
mv %{buildroot}%{_bindir}/userdb %{buildroot}%{_bindir}/userdb-maildrop
mv %{buildroot}%{_bindir}/userdbpw %{buildroot}%{_bindir}/userdbpw-maildrop
mv %{buildroot}%{_bindir}/vchkpw2userdb %{buildroot}%{_bindir}/vchkpw2userdb-maildrop

mv %{buildroot}%{_mandir}/man1/maildirmake.1 %{buildroot}%{_mandir}/man1/maildirmake-maildrop.1
mv %{buildroot}%{_mandir}/man8/userdb.8 %{buildroot}%{_mandir}/man8/userdb-maildrop.8
mv %{buildroot}%{_mandir}/man8/vchkpw2userdb.8 %{buildroot}%{_mandir}/man8/vchkpw2userdb-maildrop.8
mv %{buildroot}%{_mandir}/man8/userdbpw.8 %{buildroot}%{_mandir}/man8/userdbpw-maildrop.8
mv %{buildroot}%{_mandir}/man8/pw2userdb.8 %{buildroot}%{_mandir}/man8/pw2userdb-maildrop.8
mv %{buildroot}%{_mandir}/man8/makeuserdb.8 %{buildroot}%{_mandir}/man8/makeuserdb-maildrop.8
mv %{buildroot}%{_mandir}/man8/deliverquota.8 %{buildroot}%{_mandir}/man8/deliverquota-maildrop.8

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL NEWS UPGRADE ChangeLog maildir/README* html
%doc INSTALL.html maildroptips.txt my.mailfilter.txt
%doc README.html UPGRADE.html README.DELTAG.html
%doc maildir/README.maildirfilter.html
%doc maildir/README.maildirquota.html
%doc maildir/README.maildirquota.txt
%doc maildir/README.sharedfolders.html
%doc maildir/README.sharedfolders.txt

%attr(0755,root,mail) %dir %{_sysconfdir}/maildrop
%attr(0700,root,mail) %dir %{_sysconfdir}/maildrop/maildroprcs

%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/maildrop/autoresponsesquota
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/maildrop/maildirfilterconfig
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/maildrop/maildirshared
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/maildrop/maildroprc
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/maildrop/quotawarnmsg

%attr(0755,root,mail) %{_bindir}/lockmail
%attr(0755,root,mail) %{_bindir}/maildrop
%attr(0755,root,root) %{_bindir}/deliverquota-maildrop
%attr(0755,root,root) %{_bindir}/mailbot
%attr(0755,root,root) %{_bindir}/maildirmake-maildrop
%attr(0755,root,root) %{_bindir}/makedatprog
%attr(0755,root,root) %{_bindir}/makemime
%attr(0755,root,root) %{_bindir}/reformime
%attr(0755,root,root) %{_bindir}/subjadd

%attr(0755,root,root) %{_bindir}/makedat
%attr(0755,root,root) %{_bindir}/makeuserdb-maildrop
%attr(0755,root,root) %{_bindir}/pw2userdb-maildrop
%attr(0755,root,root) %{_bindir}/reformail
%attr(0755,root,root) %{_bindir}/userdb-maildrop
%attr(0755,root,root) %{_bindir}/userdbpw-maildrop
%attr(0755,root,root) %{_bindir}/vchkpw2userdb-maildrop

# softlinked into %{_bindir}/
%dir %{_datadir}/maildrop/
%dir %{_datadir}/maildrop/scripts/
%attr(0755,root,mail) %{_datadir}/maildrop/scripts/makedat
%attr(0755,root,mail) %{_datadir}/maildrop/scripts/makeuserdb
%attr(0755,root,mail) %{_datadir}/maildrop/scripts/pw2userdb
%attr(0755,root,mail) %{_datadir}/maildrop/scripts/userdb
%attr(0755,root,mail) %{_datadir}/maildrop/scripts/vchkpw2userdb

%attr(0644,root,root) %{_mandir}/man[1578]/*

%files mysql
%defattr(-,root,root)
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/maildrop/maildrop-mysql.config
%attr(0755,root,mail) %{_bindir}/maildrop-mysql

%files openldap
%defattr(-,root,root)
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/maildrop/maildrop-openldap.config
%attr(0755,root,mail) %{_bindir}/maildrop-openldap

%files devel
%defattr(-,root,root)
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_includedir}/*.h
%attr(0755,root,root) %{_libdir}/*.a
