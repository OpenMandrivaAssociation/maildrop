Summary:	Mail filter/mail delivery agent
Name:		maildrop
Version:	2.5.5
Release:	4
License:	GPLv3
Group:		System/Servers
URL:		https://www.courier-mta.org/maildrop/
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

%files
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


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 2.5.5-2mdv2012.0
+ Revision: 773001
- relink against libpcre.so.1

* Mon Dec 12 2011 Alexander Khrukin <akhrukin@mandriva.org> 2.5.5-1
+ Revision: 740528
- version update 2.5.5

* Fri Oct 07 2011 Oden Eriksson <oeriksson@mandriva.com> 2.5.4-1
+ Revision: 703470
- 2.5.4 (bye bye 1.7.0)

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-24
+ Revision: 645831
- relink against libmysqlclient.so.18

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-23mdv2011.0
+ Revision: 627257
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-22mdv2011.0
+ Revision: 626539
- rebuilt against mysql-5.5.8 libs

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-20mdv2011.0
+ Revision: 612792
- the mass rebuild of 2010.1 packages

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-19mdv2010.1
+ Revision: 507488
- rebuild

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-18mdv2010.1
+ Revision: 506732
- P3: security fix for CVE-2010-0301

* Mon Oct 05 2009 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-17mdv2010.0
+ Revision: 453965
- fix build (again)
- fix build
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-15mdv2009.1
+ Revision: 311306
- rebuilt against mysql-5.1.30 libs

* Mon Jul 28 2008 Thierry Vignaud <tv@mandriva.org> 1.7.0-14mdv2009.0
+ Revision: 251710
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-12mdv2008.1
+ Revision: 137510
- rebuilt against openldap-2.4.7 libs

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-11mdv2008.0
+ Revision: 83803
- rebuild

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - Import maildrop



* Mon Sep 04 2006 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Mon Apr 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-9mdk
- fix so that it really mimics qmail (thanks Markus Ueberall)
- pass -DLDAP_DEPRECATED to CFLAGS

* Tue Feb 21 2006 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-8mdk
- fix a segfault when maildropmysql.cf can not be read (P1, gentoo)

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-7mdk
- rebuilt against openssl-0.9.8a

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-6mdk
- rebuilt against MySQL-5.0.15

* Tue Aug 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1.7.0-5mdk
- rebuilt against new openldap-2.3.6 libs

* Mon Feb 07 2005 Buchan Milne <bgmilne@linux-mandrake.com> 1.7.0-4mdk
- rebuild for ldap2.2_7

* Mon Jan 24 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.7.0-3mdk 
- rebuilt against MySQL-4.1.x system libs

* Mon Oct 25 2004 Michael Scherer <misc@mandrake.org> 1.7.0-2mdk 
- [DIRM]

* Thu Aug 12 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.7.0-1mdk
- 1.7.0

* Sun Jun 20 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.6.4-0.20040608.1mdk
- use a snap from 20040608

* Sun Jun 06 2004 Michael Scherer <misc@mandrake.org> 1.6.3-2mdk 
- rebuild for new gcc

* Fri Oct 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.3-1mdk
- 1.6.3

* Tue Oct 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.1-2mdk
- added fixes by Brook Humphrey:
  - Fixed permissions

* Sun Sep 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.1-1mdk
- 1.6.1
- fix invalid-build-requires
- fix explicit-lib-dependency

* Mon Aug 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.0-1mdk
- 1.6.0
- update %%description

* Thu Aug 07 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5.3-2mdk
- added S3
- use ./Maildir as default
- readded into cooker contribs

* Mon Jul 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5.3-1mdk
- new version (it's been out for a while now...)
- added the %%{_sysconfdir}/maildrop/* stuff
- added S1, S2 & P0
- added the mysql and openldap sub packages

* Thu Mar  6 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.4.0-2rph
- rebuild for 9.1
- include some missing files

* Mon Aug 12 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.0-1mdk
- new version (it's been out for a while now...)

* Fri Aug  9 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.3.9-2rph
- rebuild for 9.0

* Fri Jun  7 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.3.9-1rph
- 1.3.9
- merge maildrop-man into main maildrop package
- some spec cleanups
- change Group for maildrop-devel
- BuildRequires: libgdbm-devel
- first rpmhelp.net package

* Wed Mar 20 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.8-1mdk
- 1.3.8

* Wed Jan 09 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.3.7-1mdk
- 1.3.7

* Wed Nov 28 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.3.6-1mdk
- 1.3.6

* Tue Aug 21 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.3.4-1mdk
- updated to 1.3.4

* Mon Jan 22 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.2.2-2mdk
- rebuild

* Thu Nov 23 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.2.2-1mdk
- new in contribs
