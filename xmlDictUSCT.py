#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mthornton
#
# Created:     03/03/2017
# Copyright:   (c) mthornton 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

'''
<nc:DocumentPostDate>       Req     Mailing date of the notice
<nc:DateTime>               Req     Date and Time Format
<ebn:BankruptcyFilingDate>
                <nc:Date>   Opt     The filing date
<nc:CaseTitleText>          Req     Typically the debtor's name or the title used for ?In re?
<nc:CaseDocketID>           Req     Case number
<j: j:CaseAugmentation>
            <j:CaseCourt>   Req     Court that originated the notice
<ecf:CaseAugmentation> Req Start of role information.
<ecf:Alias> Opt
<ecf:AliasAlternateName> Opt Could be multiple instances
<ecf:AliasAlternateNameTypeCode> Opt Type of Alias ? See Code List
<nc:EntityReference> Req Role information
<ecf:CaseParticipant
< ecf:EntityOrganization OR
ecf:EntityPerson>
< ecf:OrganizationName OR
nc:PersonName>
Req Dependent upon individual or business ;
identified by SSN or TaxID
<nc:OrganizationName>
<nc:AddressRecipientName>
<nc:PersonGivenName> Opt First Name
<nc:PersonMiddleName> Opt Used even if only middle initial is
provided
<nc:PersonSurName> Opt Last Name
<nc:PersonSuffixNameText> Opt Generation or other suffix
<bankruptcy:AssetNoticeIndicator> True or
False
Opt Indicates if this is an asset case.
<bankruptcy:JointPetitionIndicator> True or
False
Req True if Joint Debtor Case

'''


'''
XML Property List
The following description is not meant as a replacement for the document type definition (DTD). It is
provided as a convenience in a more easily readable format. Property Tags can be traced to their source
standard by the following key:
nc ? NIEM Core
j ? Justice Domain within NIEM
ecf ? Electronic Case Filing standard maintained by OASIS
bankruptcy ? subset of ecf
ebn ? Extensions defined by the Bankruptcy Noticing Center for notices

<ebn:EBNBatch>          Req     Opening and closing to allow for multiple notices within a PDF if a user
receives this format. Present for single
notice PDF files also.

<CoreFilingMessage>             The IEPD identifier for Legal XML that
starts a transaction.
<nc:DocumentIdentification> Req
<nc:IdentificationID>       Req 1 ?As part of document ID: This number
                                has 4 segments separated by a dash,
                                tpseq-sequence_number-batch-item.
                                The sequence number should be used
                                by the recipient to ensure all documents
                                received. Batch and item identifiers are
                                primarily for BNC use.
                                2 ? As part of SendingMDELocationID: Always ?BNC?
                                3 ? As part of the court location: Court identifier.
<nc:DocumentPostDate>       Req Mailing date of the notice
<nc:DocumentPostDate>       Req Mailing date of the notice
<nc:DateTime>               Req Date and Time Format
<ecf:SendingMDELocationID>  Req Indicates who sent the document,
                                notices from BNC will have ?BNC?
<ecf:SendingMDEProfileCode> Req Provided for ECF compliance.
<ebn:BankruptcyFilingDate>
<nc:Date>                   Opt The filing date
<nc:CaseTitleText>          Req Typically the debtor's name or the title used for ?In re?
<nc:CaseCategoryText>       Req See Code List
<nc:CaseDocketID>           Req Case number
<j: j:CaseAugmentation>
<j:CaseCourt>               Req Court that originated the notice


'''
