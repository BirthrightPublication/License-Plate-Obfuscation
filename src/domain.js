export const states = "Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming".split('|');
export const statuses = ['Legal','Illegal','Obscure','Unverified'];
export const risks = ['1 — Minimal','2 — Low','3 — Moderate','4 — High','5 — Critical'];
export const sources = {
 California: {catalog:'https://www.dmv.ca.gov/portal/vehicle-registration/license-plates-decals-and-placards/', law:'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=5201.&lawCode=VEH', title:'California Vehicle Code §5201', rule:'California generally requires plates to remain clearly visible and legible. Review the current text and exceptions.', validation:'https://www.dmv.ca.gov/portal/vehicle-registration/license-plates-decals-and-placards/personalized-license-plates/'},
 Texas: {catalog:'https://www.txdmv.gov/motorists/license-plates', law:'https://statutes.capitol.texas.gov/Docs/TN/htm/TN.504.htm#504.945', title:'Texas Transportation Code §504.945', rule:'Texas regulates obscuring or altering plate information. Review the current text and exceptions.'},
 'New York': {catalog:'https://dmv.ny.gov/plates', law:'https://www.nysenate.gov/legislation/laws/VAT/402', title:'New York Vehicle and Traffic Law §402', rule:'New York regulates plate display and legibility. Review the current text and exceptions.'}
};
export function validate(state,text) {
 if (!states.includes(state)) return {status:'invalid',message:'Choose a state.'};
 if (!text || text.length > 12 || !/^[A-Z0-9 -]+$/.test(text)) return {status:'invalid',message:'Preview accepts 1–12 uppercase letters, digits, spaces or hyphens.'};
 return {status:'unverified',message:'Preview text only. Jurisdiction-specific eligibility rules are not verified; consult the issuing authority.'};
}
export function legalRecord(state) { return {classification:'Unverified',risk:null,source:sources[state]??null,verifiedAt:null,explanation:'No current legal review has been completed. A source link is a research lead, not verified legal advice.'}; }
export function availability() { return {status:'unavailable',message:'No authorized availability provider configured. No lookup was sent; this does not mean a plate is available.'}; }
export function parseProject(value) {
 if (!value || value.schemaVersion!==1 || !states.includes(value.state) || typeof value.text!=='string' || value.text.length>12 || typeof value.name!=='string' || value.name.length>80) throw Error('Unsupported or invalid project');
 return {schemaVersion:1,name:value.name,state:value.state,text:value.text};
}
