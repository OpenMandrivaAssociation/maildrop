Summary:	Maildrop mail filter/mail delivery agent
Name:		maildrop
Version:	2.5.5
Release:	%mkrel 2
License:	GPLv3
Group:		System/Servers
URL:		http://www.courier-mta.org/maildrop/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		maildrop-1.7.0-format_not_a_string_literal_and_no_format_arguments.diff
BuildConflicts:	libreoffice-common
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-devel
BuildRequires:	fam-devel
BuildRequires:	idn-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pcre-devel
Requires:	sendmail-command

%description
Maildrop is a combination mail filter/mail delivery agent. Maildrop reads the
message to be delivered to your mailbox, optionally reads instructions from a
file how filter incoming mail, then based on these instructions may deliver
mail to an alternate mailbox, or forward it, instead of dropping the message
into your mailbox.

Maildrop uses a structured, real, meta-programming language in order to define
filtering instructions. Its basic features are fast and efficient. At sites
which carry a light load, the more advanced, CPU-demanding, features can be
used to build very sophisticated mail filters.  Maildrop deployments have
been reported at sites that support as many as 30,000 mailboxes.

Maildrop mailing list:
http://lists.sourceforge.net/lists/listinfo/courier-maildrop

This version is compiled with support for GDBM database files, maildir
enhancements (folders+quotas), and userdb.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

%build
export DEFAULT_DEF="./Maildir"
export MAILBOT="%{_bindir}/mailbot"

%configure2_5x \
    --disable-authlib \
    --enable-crlf-term=1 \
    --enable-global-timeout=300 \
    --enable-keep-fromline=1 \
    --enable-lockext-def=.lock \
    --enable-lockrefresh-def=15 \
    --enable-locksleep-def=5 \
    --enable-locktimeout-def=60 \
    --enable-maildirquota \
    --enable-maildrop-gid=mail \
    --enable-maildrop-uid=root \
    --enable-mimecharset=iso-8859-1 \
    --enable-restrict-trusted=0 \
    --enable-sendmail=%{_sbindir}/sendmail \
    --enable-smallmsg=8192 \
    --enable-syslog=1 \
    --enable-tempdir=.tmp \
    --enable-trusted-users="root mail daemon postfix postmaster uucp qmaild sendmail mmdf vpopmaill" \
    --enable-use-flock=1 \
    --with-db=db \
    --with-dirsync \
    --with-etcdir=%{_sysconfdir}/maildrop \
    --with-libidn=%{_prefix} \
    --without-devel \
    --with-trashquota

%make

%install
rm -rf %{buildroot}

%makeinstall_std MAILDROPUID='' MAILDROPGID=''

install -d %{buildroot}%{_sysconfdir}/maildrop/maildroprcs

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
rm -rf html
mv %{buildroot}%{_datadir}/maildrop/html html

# fix so that these won't conflict with the courier-imap package
mv %{buildroot}%{_bindir}/deliverquota %{buildroot}%{_bindir}/deliverquota-maildrop
mv %{buildroot}%{_bindir}/maildirmake %{buildroot}%{_bindir}/maildirmake-maildrop

mv %{buildroot}%{_mandir}/man1/maildirmake.1 %{buildroot}%{_mandir}/man1/maildirmake-maildrop.1
mv %{buildroot}%{_mandir}/man8/deliverquota.8 %{buildroot}%{_mandir}/man8/maildirmake-deliverquota.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL NEWS UPGRADE ChangeLog maildir/README* html
%doc INSTALL.html maildroptips.txt
%doc README.html UPGRADE.html
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
%attr(0755,root,root) %{_bindir}/makedat
%attr(0755,root,root) %{_bindir}/reformail

%attr(0644,root,root) %{_mandir}/man[1578]/*
